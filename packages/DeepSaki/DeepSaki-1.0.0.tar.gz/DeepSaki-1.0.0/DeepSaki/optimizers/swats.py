from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from typing import Any
from typing import Dict
from typing import List

import tensorflow as tf
from tensorflow.python.framework import ops
from tensorflow.python.keras import backend_config
from tensorflow.python.keras.optimizer_v2 import optimizer_v2
from tensorflow.python.ops import array_ops
from tensorflow.python.ops import control_flow_ops
from tensorflow.python.ops import math_ops
from tensorflow.python.ops import state_ops
from tensorflow.python.ops import variables as tf_variables
from tensorflow.python.training import gen_training_ops

from DeepSaki.types.optimizers_enums import CurrentOptimizer

class SwatsAdam(optimizer_v2.OptimizerV2):
    """Initializer that can switch from ADAM to SGD and vice versa.

    SWATS_ADAM is inspired by the [SWATS](http://arxiv.org/abs/1712.07628) (switching from adam to sgd) initializer.
    During training, the optimizer can be changed by calling `switch_optimizer()` uppon the optimizer instance.

    This optimizer combines tensorflow's [ADAM](https://github.com/tensorflow/tensorflow/blob/85c8b2a817f95a3e979ecd1ed95bff1dc1335cff/tensorflow/python/keras/optimizer_v2/adam.py)
    and [SGD](https://github.com/tensorflow/tensorflow/blob/85c8b2a817f95a3e979ecd1ed95bff1dc1335cff/tensorflow/python/keras/optimizer_v2/gradient_descent.py) implementations.

    **Example:**
    ```python
    import DeepSaki as ds
    optimizer = ds.optimizer.SWATS_ADAM(learning_rate=disc_learning_rate, beta_1=0.5, amsgrad=False, momentum=0.9, nesterov=False)
    optimizer.switch_optimizer()
    ```
    """

    _HAS_AGGREGATE_GRAD = True

    def __init__(
        self,
        learning_rate: float = 0.001,
        beta_1: float = 0.9,
        beta_2: float = 0.999,
        epsilon: float = 1e-7,
        amsgrad: bool = False,
        momentum: float = 0.0,
        nesterov: bool = False,
        **kwargs: Any,
    ) -> None:
        """Initializes the `SwatsAdam` optimizer.

        Args:
            learning_rate (float, optional): Learning rate of the optimization step. Defaults to 0.001.
            beta_1 (float, optional): The exponential decay rate for the 1st moment estimates. Defaults to 0.9.
            beta_2 (float, optional): The exponential decay rate for the 2nd moment estimates. Defaults to 0.999.
            epsilon (float, optional): A small constant for numerical stability. Defaults to 1e-7.
            amsgrad (bool, optional): Whether to apply AMSGrad variant of this algorithm from the paper "On the
                Convergence of Adam and beyond". Defaults to False.
            momentum (float, optional):  Hyperparameter >= 0 that accelerates gradient descent in the relevant direction
                and dampens oscillations. Vanilla gradient descent means no momentum. Defaults to 0.0.
            nesterov (bool, optional): Whether to apply Nesterov momentum. Defaults to False.
            kwargs: keyword arguments passed to the parent class.

        Raises:
            ValueError: if `momentum` is not provided in an expected form.
        """
        super(SwatsAdam, self).__init__(name="SwatsAdam", **kwargs)
        self._set_hyper("learning_rate", kwargs.get("lr", learning_rate))
        self._set_hyper("decay", self._initial_decay)
        self._set_hyper("beta_1", beta_1)
        self._set_hyper("beta_2", beta_2)
        self.epsilon = epsilon or backend_config.epsilon()
        self.amsgrad = amsgrad
        self.currentOptimizer = CurrentOptimizer.ADAM

        self._momentum = False
        if isinstance(momentum, ops.Tensor) or callable(momentum) or momentum > 0:
            self._momentum = True
        if isinstance(momentum, (int, float)) and (momentum < 0 or momentum > 1):
            raise ValueError("`momentum` must be between [0, 1].")
        self._set_hyper("momentum", momentum)

        self.nesterov = nesterov

    def switch_optimizer(self) -> None:
        """Switches the current optimizer to either ADAM or SGD, depending on what was previously set."""
        if self.currentOptimizer == CurrentOptimizer.ADAM:
            self.currentOptimizer = CurrentOptimizer.SGD
        else:
            self.currentOptimizer = CurrentOptimizer.ADAM

    def _create_slots(self, var_list: List[tf.Variable]) -> None:
        # Create slots for the first and second moments.
        # Separate for-loops to respect the ordering of slot variables from v1.
        for var in var_list:
            self.add_slot(var, "m")
        for var in var_list:
            self.add_slot(var, "v")
        if self.amsgrad:
            for var in var_list:
                self.add_slot(var, "vhat")
        if self._momentum:
            for var in var_list:
                self.add_slot(var, "momentum")

    def _prepare_local(self, var_device, var_dtype: tf.DType, apply_state) -> None:
        super(SwatsAdam, self)._prepare_local(var_device, var_dtype, apply_state)

        local_step = math_ops.cast(self.iterations + 1, var_dtype)
        beta_1_t = array_ops.identity(self._get_hyper("beta_1", var_dtype))
        beta_2_t = array_ops.identity(self._get_hyper("beta_2", var_dtype))
        beta_1_power = math_ops.pow(beta_1_t, local_step)
        beta_2_power = math_ops.pow(beta_2_t, local_step)
        lr = apply_state[(var_device, var_dtype)]["lr_t"] * (math_ops.sqrt(1 - beta_2_power) / (1 - beta_1_power))
        apply_state[(var_device, var_dtype)].update(
            {
                "lr": lr,
                "epsilon": ops.convert_to_tensor_v2_with_dispatch(self.epsilon, var_dtype),
                "beta_1_t": beta_1_t,
                "beta_1_power": beta_1_power,
                "one_minus_beta_1_t": 1 - beta_1_t,
                "beta_2_t": beta_2_t,
                "beta_2_power": beta_2_power,
                "one_minus_beta_2_t": 1 - beta_2_t,
            }
        )

        apply_state[(var_device, var_dtype)]["momentum"] = array_ops.identity(self._get_hyper("momentum", var_dtype))

    def set_weights(self, weights) -> None:
        params = self.weights
        # If the weights are generated by Keras V1 optimizer, it includes vhats
        # even without amsgrad, i.e, V1 optimizer has 3x + 1 variables, while V2
        # optimizer has 2x + 1 variables. Filter vhats out for compatibility.
        num_vars = int((len(params) - 1) / 2)
        if len(weights) == 3 * num_vars + 1:
            weights = weights[: len(params)]
        super(SwatsAdam, self).set_weights(weights)

    def _resource_apply_dense(self, grad, var, apply_state=None):
        var_device, var_dtype = var.device, var.dtype.base_dtype
        coefficients = (apply_state or {}).get((var_device, var_dtype)) or self._fallback_apply_state(
            var_device, var_dtype
        )

        if self.currentOptimizer == CurrentOptimizer.SGD:
            if self._momentum:
                momentum_var = self.get_slot(var, "momentum")
                return gen_training_ops.ResourceApplyKerasMomentum(
                    var=var.handle,
                    accum=momentum_var.handle,
                    lr=coefficients["lr_t"],
                    grad=grad,
                    momentum=coefficients["momentum"],
                    use_locking=self._use_locking,
                    use_nesterov=self.nesterov,
                )

            return gen_training_ops.ResourceApplyGradientDescent(
                var=var.handle, alpha=coefficients["lr_t"], delta=grad, use_locking=self._use_locking
            )

        if self.currentOptimizer == CurrentOptimizer.ADAM:
            m = self.get_slot(var, "m")
            v = self.get_slot(var, "v")
            if not self.amsgrad:
                return gen_training_ops.ResourceApplyAdam(
                    var=var.handle,
                    m=m.handle,
                    v=v.handle,
                    beta1_power=coefficients["beta_1_power"],
                    beta2_power=coefficients["beta_2_power"],
                    lr=coefficients["lr_t"],
                    beta1=coefficients["beta_1_t"],
                    beta2=coefficients["beta_2_t"],
                    epsilon=coefficients["epsilon"],
                    grad=grad,
                    use_locking=self._use_locking,
                )

            vhat = self.get_slot(var, "vhat")
            return gen_training_ops.ResourceApplyAdamWithAmsgrad(
                var=var.handle,
                m=m.handle,
                v=v.handle,
                vhat=vhat.handle,
                beta1_power=coefficients["beta_1_power"],
                beta2_power=coefficients["beta_2_power"],
                lr=coefficients["lr_t"],
                beta1=coefficients["beta_1_t"],
                beta2=coefficients["beta_2_t"],
                epsilon=coefficients["epsilon"],
                grad=grad,
                use_locking=self._use_locking,
            )

        raise Exception("Optimizer is not Defined. Use adam or sgd.")

    def _resource_apply_sparse(self, grad, var, indices, apply_state=None):
        var_device, var_dtype = var.device, var.dtype.base_dtype
        coefficients = (apply_state or {}).get((var_device, var_dtype)) or self._fallback_apply_state(
            var_device, var_dtype
        )

        if self.currentOptimizer == CurrentOptimizer.SGD:
            momentum_var = self.get_slot(var, "momentum")
            return gen_training_ops.ResourceSparseApplyKerasMomentum(
                var=var.handle,
                accum=momentum_var.handle,
                lr=coefficients["lr_t"],
                grad=grad,
                indices=indices,
                momentum=coefficients["momentum"],
                use_locking=self._use_locking,
                use_nesterov=self.nesterov,
            )

        if self.currentOptimizer == CurrentOptimizer.ADAM:
            m = self.get_slot(var, "m")
            m_scaled_g_values = grad * coefficients["one_minus_beta_1_t"]
            m_t = state_ops.assign(m, m * coefficients["beta_1_t"], use_locking=self._use_locking)
            with ops.control_dependencies([m_t]):
                m_t = self._resource_scatter_add(m, indices, m_scaled_g_values)

            v = self.get_slot(var, "v")
            v_scaled_g_values = (grad * grad) * coefficients["one_minus_beta_2_t"]
            v_t = state_ops.assign(v, v * coefficients["beta_2_t"], use_locking=self._use_locking)
            with ops.control_dependencies([v_t]):
                v_t = self._resource_scatter_add(v, indices, v_scaled_g_values)

            if not self.amsgrad:
                v_sqrt = math_ops.sqrt(v_t)
                var_update = state_ops.assign_sub(
                    var, coefficients["lr"] * m_t / (v_sqrt + coefficients["epsilon"]), use_locking=self._use_locking
                )
                return control_flow_ops.group(*[var_update, m_t, v_t])

            v_hat = self.get_slot(var, "vhat")
            v_hat_t = math_ops.maximum(v_hat, v_t)
            with ops.control_dependencies([v_hat_t]):
                v_hat_t = state_ops.assign(v_hat, v_hat_t, use_locking=self._use_locking)
            v_hat_sqrt = math_ops.sqrt(v_hat_t)
            var_update = state_ops.assign_sub(
                var, coefficients["lr"] * m_t / (v_hat_sqrt + coefficients["epsilon"]), use_locking=self._use_locking
            )
            return control_flow_ops.group(*[var_update, m_t, v_t, v_hat_t])

        raise Exception("Optimizer is not Defined. Use adam or sgd.")

    def get_config(self) -> Dict[str, Any]:
        """Serialization of the object.

        Returns:
            Dictionary with the class' variable names as keys.
        """
        config = super(SwatsAdam, self).get_config()
        config.update(
            {
                "learning_rate": self._serialize_hyperparameter("learning_rate"),
                "decay": self._serialize_hyperparameter("decay"),
                "beta_1": self._serialize_hyperparameter("beta_1"),
                "beta_2": self._serialize_hyperparameter("beta_2"),
                "epsilon": self.epsilon,
                "amsgrad": self.amsgrad,
                "momentum": self._serialize_hyperparameter("momentum"),
                "nesterov": self.nesterov,
                "current_optimizer": self.currentOptimizer,
            }
        )
        return config


class SwatsNadam(optimizer_v2.OptimizerV2):
    """Initializer that can switch from NADAM to SGD and vice versa.

    SWATS_NADAM is inspired by the [SWATS](http://arxiv.org/abs/1712.07628) (switching from adam to sgd) initializer.
    During training, the optimizer can be changed by calling `switch_optimizer()` uppon the optimizer instance.

    This optimizer combines tensorflow's [NADAM](https://github.com/tensorflow/tensorflow/blob/85c8b2a817f95a3e979ecd1ed95bff1dc1335cff/tensorflow/python/keras/optimizer_v2/nadam.py)
    and [SGD](https://github.com/tensorflow/tensorflow/blob/85c8b2a817f95a3e979ecd1ed95bff1dc1335cff/tensorflow/python/keras/optimizer_v2/gradient_descent.py) implementations.

    **Example:**
    ```python
    import DeepSaki as ds
    optimizer = ds.optimizer.SWATS_NADAM(learning_rate=disc_learning_rate, beta_1=0.5, momentum=0.9, nesterov=False)
    optimizer.switch_optimizer()
    ```
    """

    _HAS_AGGREGATE_GRAD = True

    def __init__(
        self,
        learning_rate: float = 0.001,
        beta_1: float = 0.9,
        beta_2: float = 0.999,
        epsilon: float = 1e-7,
        momentum: float = 0.0,
        nesterov: bool = False,
        **kwargs: Any,
    ) -> None:
        """Initializes the `SwatsNadam` optimizer.

        Args:
            learning_rate (float, optional): Learning rate of the optimization step. Defaults to 0.001.
            beta_1 (float, optional): The exponential decay rate for the 1st moment estimates. Defaults to 0.9.
            beta_2 (float, optional): The exponential decay rate for the 2nd moment estimates. Defaults to 0.999.
            epsilon (float, optional): A small constant for numerical stability. Defaults to 1e-7.
            momentum (float, optional):  Hyperparameter >= 0 that accelerates gradient descent in the relevant direction
                and dampens oscillations. Vanilla gradient descent means no momentum. Defaults to 0.0.
            nesterov (bool, optional): Whether to apply Nesterov momentum. Defaults to False.
            kwargs: keyword arguments passed to the parent class.

        Raises:
            ValueError: if `momentum` is not provided in an expected form.
        """
        super(SwatsNadam, self).__init__(name="SwatsNadam", **kwargs)
        self._set_hyper("learning_rate", kwargs.get("lr", learning_rate))
        self._set_hyper("decay", self._initial_decay)
        self._set_hyper("beta_1", beta_1)
        self._set_hyper("beta_2", beta_2)
        self.epsilon = epsilon or backend_config.epsilon()
        self.currentOptimizer = CurrentOptimizer.NADAM

        self._momentum = False
        if isinstance(momentum, ops.Tensor) or callable(momentum) or momentum > 0:
            self._momentum = True
        if isinstance(momentum, (int, float)) and (momentum < 0 or momentum > 1):
            raise ValueError("`momentum` must be between [0, 1].")
        self._set_hyper("momentum", momentum)

        self.nesterov = nesterov
        self._m_cache = None

    def switch_optimizer(self) -> None:
        """Switches the current optimizer to either ADAM or SGD, depending on what was previously set."""
        if self.currentOptimizer == CurrentOptimizer.NADAM:
            self.currentOptimizer = CurrentOptimizer.SGD
        else:
            self.currentOptimizer = CurrentOptimizer.NADAM

    def _create_slots(self, var_list: List[tf.Variable]) -> None:
        # Create slots for the first and second moments.
        # Separate for-loops to respect the ordering of slot variables from v1.
        for var in var_list:
            self.add_slot(var, "m")
        for var in var_list:
            self.add_slot(var, "v")
        if self._m_cache is None:
            var_dtype = var_list[0].dtype.base_dtype
            self._m_cache = self.add_weight(
                "momentum_cache",
                shape=[],
                dtype=var_dtype,
                initializer="ones",
                trainable=False,
                aggregation=tf_variables.VariableAggregation.ONLY_FIRST_REPLICA,
            )
        self._weights.append(self._m_cache)

        if self._momentum:
            for var in var_list:
                self.add_slot(var, "momentum")

    def _prepare_local(self, var_device, var_dtype: tf.DType, apply_state) -> None:
        super(SwatsNadam, self)._prepare_local(var_device, var_dtype, apply_state)

        # From Nadam Optimizer!
        lr_t = array_ops.identity(self._get_hyper("learning_rate", var_dtype))
        beta_1_t = array_ops.identity(self._get_hyper("beta_1", var_dtype))
        beta_2_t = array_ops.identity(self._get_hyper("beta_2", var_dtype))
        local_step = math_ops.cast(self.iterations + 1, var_dtype)
        next_step = math_ops.cast(self.iterations + 2, var_dtype)
        decay_base = math_ops.cast(0.96, var_dtype)
        m_t = beta_1_t * (1.0 - 0.5 * (math_ops.pow(decay_base, self._initial_decay * local_step)))
        m_t_1 = beta_1_t * (1.0 - 0.5 * (math_ops.pow(decay_base, self._initial_decay * next_step)))
        m_schedule_new = math_ops.cast(self._m_cache_read, var_dtype) * m_t
        if var_dtype is self._m_cache.dtype:
            m_schedule_new = array_ops.identity(
                state_ops.assign(self._m_cache, m_schedule_new, use_locking=self._use_locking)
            )
        m_schedule_next = m_schedule_new * m_t_1

        apply_state[(var_device, var_dtype)] = {
            "lr_t": lr_t,
            "neg_lr_t": -lr_t,
            "epsilon": ops.convert_to_tensor_v2_with_dispatch(self.epsilon, var_dtype),
            "beta_1_t": beta_1_t,
            "beta_2_t": beta_2_t,
            "m_t": m_t,
            "m_t_1": m_t_1,
            "one_minus_beta_1_t": 1 - beta_1_t,
            "one_minus_beta_2_t": 1 - beta_2_t,
            "one_minus_m_t": 1.0 - m_t,
            "one_minus_m_schedule_new": 1.0 - m_schedule_new,
            "one_minus_m_schedule_next": 1.0 - m_schedule_next,
            "v_t_prime_denominator": 1.0 - math_ops.pow(beta_2_t, local_step),
        }

        # from SGD Optimizer
        apply_state[(var_device, var_dtype)]["momentum"] = array_ops.identity(self._get_hyper("momentum", var_dtype))

    def _prepare(self, var_list: List[tf.Variable]):
        # Get the value of the momentum cache before starting to apply gradients.
        self._m_cache_read = array_ops.identity(self._m_cache)
        return super(SwatsNadam, self)._prepare(var_list)

    def _resource_apply_dense(self, grad, var, apply_state=None):
        var_device, var_dtype = var.device, var.dtype.base_dtype
        coefficients = (apply_state or {}).get((var_device, var_dtype)) or self._fallback_apply_state(
            var_device, var_dtype
        )

        # SGD Optimizer!
        if self.currentOptimizer == CurrentOptimizer.SGD:
            if self._momentum:
                momentum_var = self.get_slot(var, "momentum")
                return gen_training_ops.ResourceApplyKerasMomentum(
                    var=var.handle,
                    accum=momentum_var.handle,
                    lr=coefficients["lr_t"],
                    grad=grad,
                    momentum=coefficients["momentum"],
                    use_locking=self._use_locking,
                    use_nesterov=self.nesterov,
                )
            return gen_training_ops.ResourceApplyGradientDescent(
                var=var.handle, alpha=coefficients["lr_t"], delta=grad, use_locking=self._use_locking
            )
        # Nadam Optimizer!
        if self.currentOptimizer == CurrentOptimizer.NADAM:
            m = self.get_slot(var, "m")
            v = self.get_slot(var, "v")
            g_prime = grad / coefficients["one_minus_m_schedule_new"]
            m_t = coefficients["beta_1_t"] * m + coefficients["one_minus_beta_1_t"] * grad
            m_t = state_ops.assign(m, m_t, use_locking=self._use_locking)
            m_t_prime = m_t / coefficients["one_minus_m_schedule_next"]
            v_t = coefficients["beta_2_t"] * v + coefficients["one_minus_beta_2_t"] * math_ops.square(grad)
            v_t = state_ops.assign(v, v_t, use_locking=self._use_locking)
            v_t_prime = v_t / coefficients["v_t_prime_denominator"]
            m_t_bar = coefficients["one_minus_m_t"] * g_prime + coefficients["m_t_1"] * m_t_prime
            var_t = var - coefficients["lr_t"] * m_t_bar / (math_ops.sqrt(v_t_prime) + coefficients["epsilon"])
            return state_ops.assign(var, var_t, use_locking=self._use_locking).op

        raise Exception("Optimizer is not Defined. Use nadam or sgd.")

    def _resource_apply_sparse(self, grad, var, indices, apply_state=None):
        var_device, var_dtype = var.device, var.dtype.base_dtype
        coefficients = (apply_state or {}).get((var_device, var_dtype)) or self._fallback_apply_state(
            var_device, var_dtype
        )

        # SGD Part
        if self.currentOptimizer == CurrentOptimizer.SGD:
            momentum_var = self.get_slot(var, "momentum")
            return gen_training_ops.ResourceSparseApplyKerasMomentum(
                var=var.handle,
                accum=momentum_var.handle,
                lr=coefficients["lr_t"],
                grad=grad,
                indices=indices,
                momentum=coefficients["momentum"],
                use_locking=self._use_locking,
                use_nesterov=self.nesterov,
            )
        # Nadam Part
        if self.currentOptimizer == CurrentOptimizer.NADAM:
            m = self.get_slot(var, "m")
            v = self.get_slot(var, "v")

            g_prime = grad / coefficients["one_minus_m_schedule_new"]

            m_scaled_g_values = grad * coefficients["one_minus_beta_1_t"]
            m_t = state_ops.assign(m, m * coefficients["beta_1_t"], use_locking=self._use_locking)

            with ops.control_dependencies([m_t]):
                m_t = self._resource_scatter_add(m, indices, m_scaled_g_values)
                m_t_slice = array_ops.gather(m_t, indices)

            m_t_prime = m_t_slice / coefficients["one_minus_m_schedule_next"]
            m_t_bar = coefficients["one_minus_m_t"] * g_prime + coefficients["m_t_1"] * m_t_prime

            v_scaled_g_values = (grad * grad) * coefficients["one_minus_beta_2_t"]
            v_t = state_ops.assign(v, v * coefficients["beta_2_t"], use_locking=self._use_locking)

            with ops.control_dependencies([v_t]):
                v_t = self._resource_scatter_add(v, indices, v_scaled_g_values)
                v_t_slice = array_ops.gather(v_t, indices)

            v_t_prime = v_t_slice / coefficients["v_t_prime_denominator"]
            v_prime_sqrt_plus_eps = math_ops.sqrt(v_t_prime) + coefficients["epsilon"]

            var_update = self._resource_scatter_add(
                var, indices, coefficients["neg_lr_t"] * m_t_bar / v_prime_sqrt_plus_eps
            )
            return control_flow_ops.group(*[var_update, m_t_bar, v_t])

        raise Exception("Optimizer is not Defined. Use nadam or sgd.")

    def get_config(self) -> Dict[str, Any]:
        """Serialization of the object.

        Returns:
            Dictionary with the class' variable names as keys.
        """
        config = super(SwatsNadam, self).get_config()
        config.update(
            {
                "learning_rate": self._serialize_hyperparameter("learning_rate"),
                "decay": self._serialize_hyperparameter("decay"),
                "beta_1": self._serialize_hyperparameter("beta_1"),
                "beta_2": self._serialize_hyperparameter("beta_2"),
                "epsilon": self.epsilon,
                "momentum": self._serialize_hyperparameter("momentum"),
                "nesterov": self.nesterov,
                "current_optimizer": self.currentOptimizer,
            }
        )
        return config
