import logging
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import tensorflow as tf
from tensorflow.python.client import device_lib

def detect_accelerator(
    gpu_memory_groth: bool = False,
) -> Tuple[
    tf.distribute.Strategy,
    str,
    Optional[Union[tf.distribute.cluster_resolver.TPUClusterResolver, List[tf.config.LogicalDevice]]],
]:
    """Detects the availability of TPUs and GPUs and connects to all available devices.

    Args:
        gpu_memory_groth (bool, optional): If true, memory is allocated on demand. Defaults to False.

    Returns:
        `strategy`: pointer to the distribution strategy configuration object
        `runtime_environment`: Info string describing the HW that might be used for conditions, i.e. "TPU, "GPU", "CPU"
        `hw_accelerator_handle`: pointer to the HW accelerator
    """
    hw_accelerator_handle = None
    tpu = None
    gpus = []
    try:
        tpu = tf.distribute.cluster_resolver.TPUClusterResolver()  # TPU detection
        hw_accelerator_handle = tpu
    except ValueError:
        if gpu_memory_groth:
            for gpu in tf.config.experimental.list_physical_devices("GPU"):
                tf.config.experimental.set_memory_growth(gpu, enable=True)
        gpus = tf.config.experimental.list_logical_devices("GPU")
        hw_accelerator_handle = gpus

    # Select appropriate distribution strategy
    if tpu is not None:
        runtime_environment = "TPU"
        tf.config.experimental_connect_to_cluster(tpu)
        tf.tpu.experimental.initialize_tpu_system(tpu)
        strategy = tf.distribute.TPUStrategy(
            tpu
        )  # Going back and forth between TPU and host is expensive. Better to run 128 batches on the TPU before reporting back.
        logging.info(f"Running on TPU {tpu.cluster_spec().as_dict()['worker']}")
    elif len(gpus) > 1:
        runtime_environment = "GPU"
        strategy = tf.distribute.MirroredStrategy([gpu.name for gpu in gpus])
        logging.info(f"Running on multiple GPUs {[gpu.name for gpu in gpus]}")
    elif len(gpus) == 1:
        runtime_environment = "GPU"
        strategy = tf.distribute.get_strategy()  # default strategy that works on CPU and single GPU
        logging.info(f"Running on single GPU {gpus[0].name}")
    else:
        runtime_environment = "CPU"
        strategy = tf.distribute.get_strategy()  # default strategy that works on CPU and single GPU
        logging.info("Running on CPU")

    logging.info(f"Number of accelerators: {strategy.num_replicas_in_sync}")
    logging.info("____________________________________________________________________________________")
    logging.info("Device List: ")
    logging.info(device_lib.list_local_devices())

    return strategy, runtime_environment, hw_accelerator_handle


def enable_xla_acceleration() -> None:
    """Enable compiler acceleration for linear algebra operations."""
    tf.config.optimizer.set_jit(enabled="autoclustering")
    logging.info("Linear algebra acceleration enabled")


def enable_mixed_precision() -> None:
    """Set mixed precission policy depending on the available HW accelerator. TPU:`mixed_bfloat16`. GPU:`mixed_float16`."""
    try:
        tpu = tf.distribute.cluster_resolver.TPUClusterResolver()  # TPU detection
    except ValueError:
        tpu = None

    policy_config = "mixed_bfloat16" if tpu else "mixed_float16"
    policy = tf.keras.mixed_precision.Policy(policy_config)
    tf.keras.mixed_precision.set_global_policy(policy)
    logging.info(f"Mixed precision enabled to {policy_config}")
