import tensorflow as tf

from DeepSaki.types.layers_enums import PaddingType,DownSampleType,UpSampleType,LinearLayerType
from DeepSaki.layers.sub_model_composites import Encoder, Decoder,Bottleneck
from DeepSaki.layers.layer_composites import Conv2DBlock, DenseBlock, ScalarGatedSelfAttention
from DeepSaki.layers.pooling import GlobalSumPooling2D

from typing import Tuple, Optional

class LayoutContentDiscriminator(tf.keras.Model):
    """Discriminator/critic model with two outputs to enforce disentanglement of layout and content discrimination.

    Usually used in a GAN framework.

    Info:
        Implementation as used in the [VoloGAN paper](https://arxiv.org/abs/2207.09204).

    Limitations:
        For now the input height and width of a tensor of shape (batch, height, width, channels) must be at least
        256x256

    Architecture:
        ```mermaid
        flowchart LR
        i([Input])-->e1
        subgraph Encoder
        e1-->e2-->e3-->sa[Self-Attention]
        end
        subgraph "Content Branch"
        sa-->c1-->c2-->c3-->c4
        end
        subgraph "Layout Branch"
        sa-->l1-->l2-->l3-->l4
        end
        l4-->lo([layout])
        c4-->co([content])
        ```

    **Example:**
    ```python
    import DeepSaki as ds
    import tensorflow as tf
    inputs = tf.keras.layers.Input(shape = (256,256,4))
    model = tf.keras.Model(inputs=inputs, outputs=ds.models.LayoutContentDiscriminator().call(inputs))
    model.summary()
    tf.keras.utils.plot_model(model, show_shapes=True, expand_nested=True, show_dtype=True, to_file='Unet_discriminator_model.png')
    ```
    """
    def __init__(self,
                filters:int = 64,
                downsampling:DownSampleType = DownSampleType.CONV_STRIDE_2,
                kernels:int = 3,
                first_kernel:int = 5,
                split_kernels:bool = False,
                number_of_blocks:int = 2,
                activation:str = "leaky_relu",
                dropout_rate:float = 0.2,
                use_spec_norm:bool=False,
                use_bias:bool = True,
                padding:PaddingType=PaddingType.ZERO,
                linear_layer_type:LinearLayerType = LinearLayerType.MLP,
                use_self_attention:bool = False,
                kernel_initializer:Optional[tf.keras.initializers.Initializer] = None,
                gamma_initializer:Optional[tf.keras.initializers.Initializer] = None
                ):
        """Initialize the `LayoutContentDiscriminator` object.

        Args:
            filters (int, optional): Number of filters for the initial encoder block. Defaults to 64.
            downsampling (DownSampleType, optional): Describes the downsampling method. Defaults to DownSampleType.CONV_STRIDE_2.
            kernels (int, optional): Size of the convolutions kernels. Defaults to 3.
            first_kernel (int, optional): The first convolution can have a different kernel size, to e.g. increase the
                perceptive field, while the channel depth is still low. Defaults to 5.
            split_kernels (bool, optional): To decrease the number of parameters, a convolution with the kernel_size
                `(kernel,kernel)` can be splitted into two consecutive convolutions with the kernel_size `(kernel,1)` and
                `(1,kernel)` respectivly. Defaults to False.
            number_of_blocks (int, optional): Number of consecutive convolutional building blocks, i.e. `Conv2DBlock`.
                Defaults to 2.
            activation (str, optional): String literal or tensorflow activation function object to obtain activation
                function. Defaults to "leaky_relu".
            dropout_rate (float, optional): Probability of the dropout layer. If the preceeding layer has more than one
                channel, spatial dropout is applied, otherwise standard dropout. Defaults to 0.2.
            use_spec_norm (bool, optional): Applies spectral normalization to convolutional and dense layers. Defaults to
                False.
            use_bias (bool, optional): Whether convolutions and dense layers include a bias or not. Defaults to True.
            padding (PaddingType, optional): Padding type. Defaults to PaddingType.NONE.
            linear_layer_type (LinearLayerType, optional): Determines whether 1x1 convolutions are replaced by linear
                layers, which gives the same result, but linear layers are faster. Option: LinearLayerType.MLP or
                LinearLayerType.CONV_1x1. Defaults to LinearLayerType.MLP.
            use_self_attention (bool, optional): Determines whether to apply self-attention in the decoder. Defaults to
                False.
            kernel_initializer (tf.keras.initializers.Initializer, optional): Initialization of the convolutions kernels.
                Defaults to None.
            gamma_initializer (tf.keras.initializers.Initializer, optional): Initialization of the normalization layers.
                Defaults to None.

        Raises:
            ValueError: If provided parameter for `linear_layer_type` is not supported.
        """
        super(LayoutContentDiscriminator, self).__init__()

        self.input_spec = tf.keras.layers.InputSpec(ndim=4)

        self.encoder = Encoder(number_of_levels=3, filters=filters, limit_filters=1024, downsampling=downsampling, kernels=kernels, split_kernels=split_kernels, number_of_blocks=number_of_blocks,activation=activation, first_kernel=first_kernel,use_ResidualBlock=False,channel_list=[4*filters,4*filters,8*filters],use_spec_norm=use_spec_norm, padding = padding, use_bias = use_bias, kernel_initializer = kernel_initializer, gamma_initializer = gamma_initializer)
        if use_self_attention:
            self.SA = ScalarGatedSelfAttention(use_spec_norm=use_spec_norm, intermediate_channel=None, kernel_initializer = kernel_initializer, gamma_initializer = gamma_initializer)
        else:
            self.SA = None

        if linear_layer_type == LinearLayerType.MLP:
            self.cont1 = DenseBlock(units = filters * 8, use_spec_norm = use_spec_norm, number_of_blocks = number_of_blocks, activation = activation, dropout_rate =dropout_rate, use_bias = use_bias, kernel_initializer = kernel_initializer, gamma_initializer = gamma_initializer)
            self.cont2 = DenseBlock(units = filters * 8, use_spec_norm = use_spec_norm, number_of_blocks = number_of_blocks, activation = activation, dropout_rate =dropout_rate, use_bias = use_bias, kernel_initializer = kernel_initializer, gamma_initializer = gamma_initializer)
            self.cont3 = DenseBlock(units = filters * 8, use_spec_norm = use_spec_norm, number_of_blocks = number_of_blocks, activation = activation, dropout_rate =0, final_activation=False, apply_final_normalization = False, use_bias = use_bias, kernel_initializer = kernel_initializer, gamma_initializer = gamma_initializer)
        elif linear_layer_type == LinearLayerType.CONV_1x1:
            self.cont1 = Conv2DBlock(filters=filters * 8, kernels = 1, activation = activation, split_kernels = split_kernels,number_of_blocks=number_of_blocks, dropout_rate=dropout_rate,use_spec_norm=use_spec_norm, padding=padding,use_bias = use_bias, kernel_initializer = kernel_initializer, gamma_initializer = gamma_initializer)
            self.cont2 = Conv2DBlock(filters=filters * 8, kernels = 1, activation = activation, split_kernels = split_kernels,number_of_blocks=number_of_blocks, dropout_rate=dropout_rate,use_spec_norm=use_spec_norm, padding=padding,use_bias = use_bias, kernel_initializer = kernel_initializer, gamma_initializer = gamma_initializer)
            self.cont3 = Conv2DBlock(filters=filters * 8, kernels = 1, activation = activation, split_kernels = split_kernels,number_of_blocks=number_of_blocks, dropout_rate=0,use_spec_norm=use_spec_norm, final_activation=False, apply_final_normalization = False, padding=padding,use_bias = use_bias, kernel_initializer = kernel_initializer, gamma_initializer = gamma_initializer)
        else:
            raise ValueError(f"{linear_layer_type=} is not defined.")

        self.lay1 = Conv2DBlock(filters=1, kernels = kernels, activation = activation, split_kernels = split_kernels,number_of_blocks=number_of_blocks, dropout_rate=0,use_spec_norm=use_spec_norm, padding=padding, use_bias = use_bias, kernel_initializer = kernel_initializer, gamma_initializer = gamma_initializer)
        self.lay2 = Conv2DBlock(filters=1, kernels = kernels, activation = activation, split_kernels = split_kernels,number_of_blocks=number_of_blocks, dropout_rate=dropout_rate,use_spec_norm=use_spec_norm, padding=padding,use_bias = use_bias, kernel_initializer = kernel_initializer, gamma_initializer = gamma_initializer)
        self.lay3 = Conv2DBlock(filters=1, kernels = kernels, activation = activation, split_kernels = split_kernels,number_of_blocks=number_of_blocks, dropout_rate=dropout_rate,use_spec_norm=use_spec_norm, padding=padding,use_bias = use_bias, kernel_initializer = kernel_initializer, gamma_initializer = gamma_initializer)
        self.lay4 = Conv2DBlock(filters=1, kernels = kernels, activation = activation, split_kernels = split_kernels,number_of_blocks=number_of_blocks, dropout_rate=0,use_spec_norm=use_spec_norm,final_activation=False, apply_final_normalization = False, padding=padding,use_bias = use_bias, kernel_initializer = kernel_initializer, gamma_initializer = gamma_initializer)
        #To enable mixed precission support for matplotlib and distributed training and to increase training stability
        self.linear_dtype = tf.keras.layers.Activation("linear", dtype = tf.float32)

    def build(self, input_shape:tf.TensorShape)->None:
        _, height, width,_ = input_shape
        if height < 256 or width < 256:
            raise ValueError(f"Input requires a height and width of minimum 256, but got {height=} and {width=}")

    def call(self, inputs:tf.Tensor)->Tuple[tf.Tensor,tf.Tensor]:
        """Calls the `LayoutContentDiscriminator` model.

        Args:
            inputs (tf.Tensor): Tensor of shape `(batch, height, width, channel)`.

        Returns:
            content_output: Tensor of shape `(batch, 1, 1, C)` focusing on the content of an image rather than the position.
                `C` is `filters`*2**3, where 3 is the number of downsampling blocks in the Encoder().
            layout_output: Tensor of shape `(batch, H, W, 1)` focusing on the input's layout by reducing its number of
                channels to 1. `H`=`height`/(2^3) and `W`=`width`/(2^3)
        """
        x = inputs
        encoder_out = self.encoder(x)
        if self.SA is not None:
            encoder_out = self.SA(encoder_out)

        _, pool_height, pool_width, _ = encoder_out.shape
        out1 = tf.keras.layers.AveragePooling2D(pool_size=(pool_height, pool_width))(encoder_out)
        out1 = self.cont1(out1)
        out1 = self.cont2(out1)
        out1 = self.cont3(out1)
        out1 = self.linear_dtype(out1)

        out2 = self.lay1(encoder_out)
        out2 = self.lay2(out2)
        out2 = self.lay3(out2)
        out2 = self.lay4(out2)
        out2 = self.linear_dtype(out2)

        return out1, out2

class PatchDiscriminator(tf.keras.Model):
    """Discriminator/critic model with patched output rather than single value.

    Usually used in a GAN framework.

    Architecture:
        ```mermaid
        flowchart LR
        i([Input])-->e1
        subgraph Encoder
        e1-->e2-->ex
        end
        ex-->conv1-->conv2-->o([output])

        ```

    **Example:**
    ```python
    import DeepSaki as ds
    import tensorflow as tf
    inputs = tf.keras.layers.Input(shape = (256,256,4))
    model = tf.keras.Model(inputs=inputs, outputs=ds.models.PatchDiscriminator().call(inputs))
    model.summary()
    tf.keras.utils.plot_model(model, show_shapes=True, expand_nested=True, show_dtype=True, to_file='PatchDiscriminator_model.png')
    ```

    """
    def __init__(self,
                filters:int = 64,
                downsampling:DownSampleType = DownSampleType.AVG_POOLING,
                kernels:int = 3,
                first_kernel:int = 5,
                split_kernels:bool = False,
                number_of_blocks:int = 2,
                activation:str = "leaky_relu",
                num_down_blocks:int = 3,
                dropout_rate:float = 0.2,
                use_spec_norm:bool= False,
                use_bias:bool = True,
                use_self_attention:bool=False,
                padding:PaddingType=PaddingType.ZERO,
                kernel_initializer:Optional[tf.keras.initializers.Initializer] = None,
                gamma_initializer:Optional[tf.keras.initializers.Initializer] = None
                ):
        """Initialize the `PatchDiscriminator` object.

        Args:
            filters (int, optional): Number of filters for the initial encoder block. Defaults to 64.
            downsampling (DownSampleType, optional): Describes the downsampling method. Defaults to DownSampleType.AVG_POOLING.
            kernels (int, optional): Size of the convolutions kernels. Defaults to 3.
            first_kernel (int, optional): The first convolution can have a different kernel size, to e.g. increase the
                perceptive field, while the channel depth is still low. Defaults to 5.
            split_kernels (bool, optional): To decrease the number of parameters, a convolution with the kernel_size
                `(kernel,kernel)` can be splitted into two consecutive convolutions with the kernel_size `(kernel,1)` and
                `(1,kernel)` respectivly. Defaults to False.
            number_of_blocks (int, optional): Number of consecutive convolutional building blocks, i.e. `Conv2DBlock`.
                Defaults to 2.
            activation (str, optional): String literal or tensorflow activation function object to obtain activation
                function. Defaults to "leaky_relu".
            num_down_blocks (int, optional): Number of levels in the encoder that performs a downsampling operation at its
                end. Defaults to 3.
            dropout_rate (float, optional): Probability of the dropout layer. If the preceeding layer has more than one
                channel, spatial dropout is applied, otherwise standard dropout. Defaults to 0.2.
            use_spec_norm (bool, optional): Applies spectral normalization to convolutional and dense layers. Defaults to
                False.
            use_bias (bool, optional): Whether convolutions and dense layers include a bias or not. Defaults to True.
            use_self_attention (bool, optional): Determines whether to apply self-attention in the decoder. Defaults to
                False.
            padding (PaddingType, optional): Padding type. Defaults to PaddingType.NONE.
            kernel_initializer (tf.keras.initializers.Initializer, optional): Initialization of the convolutions kernels.
                Defaults to None.
            gamma_initializer (tf.keras.initializers.Initializer, optional): Initialization of the normalization layers.
                Defaults to None.
        """
        super(PatchDiscriminator, self).__init__()

        self.input_spec = tf.keras.layers.InputSpec(ndim=4)

        self.encoder = Encoder(number_of_levels=num_down_blocks, filters=filters, limit_filters=512,  downsampling=downsampling, kernels=kernels, split_kernels=split_kernels,number_of_blocks=number_of_blocks,activation=activation,first_kernel=first_kernel,use_spec_norm=use_spec_norm,use_self_attention=use_self_attention, use_bias = use_bias,padding = padding, kernel_initializer = kernel_initializer, gamma_initializer = gamma_initializer)
        self.conv1 = Conv2DBlock(filters = filters * (2**(num_down_blocks)),  kernels = kernels, split_kernels = split_kernels, number_of_blocks = number_of_blocks, activation = activation,dropout_rate=dropout_rate,use_spec_norm=use_spec_norm, use_bias = use_bias,padding = padding, kernel_initializer = kernel_initializer, gamma_initializer = gamma_initializer)
        self.conv2 = Conv2DBlock(filters = 1, kernels = 5, split_kernels  = False, number_of_blocks = 1, activation = None,use_spec_norm=use_spec_norm, apply_final_normalization = False, use_bias = use_bias,padding = padding, kernel_initializer = kernel_initializer, gamma_initializer = gamma_initializer)
        #To enable mixed precission support for matplotlib and distributed training and to increase training stability
        self.linear_dtype = tf.keras.layers.Activation("linear", dtype = tf.float32)

    def call(self, inputs:tf.Tensor)->tf.Tensor:
        """Calls the `PatchDiscriminator` model.

        Args:
            inputs (tf.Tensor): Tensor of shape `(batch, height, width, channel)`.

        Returns:
            tf.Tensor: Tensor of shape `(batch, height//2**`number_of_blocks`, width//2**`number_of_blocks`, 1)`.
        """
        x = inputs
        x = self.encoder(x)
        x = self.conv1(x)
        x = self.conv2(x)
        return self.linear_dtype(x)

class UNetDiscriminator(tf.keras.Model):
    """U-Net based discriminator for pixel-wise real/fake prediction plus additional output for global prediction.

    Usually used in a GAN framework.

    Info:
        Implementation as used in the [VoloGAN paper](https://arxiv.org/abs/2207.09204).

    Architecture:
        ```mermaid
        flowchart LR
        i([Input])-->e1
        subgraph Encoder
        e1-->e2-->e3-->ex
        end
        subgraph Bottleneck
        ex-->b1-->bx
        end
        bx-->gp[GlobalSumPooling]-->sn[SPecNorm]-->eo([Global Prediction])
        subgraph Decoder
        bx-->dx-->d3-->d2-->d1
        end
        d1-->o([Pixel-Wise Prediction])
        e1-->d1
        e2-->d2
        e3-->d3
        ex-->dx
        ```

    **Example:**
    ```python
    import DeepSaki as ds
    import tensorflow as tf
    inputs = tf.keras.layers.Input(shape = (256,256,4))
    model = tf.keras.Model(inputs=inputs, outputs=ds.models.UNetDiscriminator(5).call(inputs))
    model.summary()
    tf.keras.utils.plot_model(model, show_shapes=True, expand_nested=True, show_dtype=True, to_file='model.png')
    ```
    """
    def __init__(self,
                number_of_levels:int= 4,
                upsampling:UpSampleType = UpSampleType.TRANSPOSE_CONV,
                downsampling:DownSampleType = DownSampleType.AVG_POOLING,
                kernels:int = 3,
                first_kernel:int = 5,
                split_kernels:bool = False,
                number_of_blocks:int = 2,
                activation:str = "leaky_relu",
                use_ResidualBlock:bool = False,
                residual_cardinality:int = 1,
                limit_filters:int = 512,
                n_bottleneck_blocks:int = 1,
                filters:int = 64,
                dropout_rate:float = 0.2,
                use_self_attention:bool=False,
                use_spec_norm:bool=False,
                use_bias:bool= True,
                linear_layer_type:LinearLayerType = LinearLayerType.MLP,
                padding:PaddingType=PaddingType.ZERO,
                kernel_initializer:Optional[tf.keras.initializers.Initializer] = None,
                gamma_initializer:Optional[tf.keras.initializers.Initializer] =  None
                ):
        """Initialize the `UNetDiscriminator` object.

        Args:
            number_of_levels (int, optional): Number of down and upsampling levels of the model. Defaults to 4.
            upsampling (UpSampleType, optional): Describes the upsampling method used. Defaults to UpSampleType.TRANSPOSE_CONV.
            downsampling (DownSampleType, optional): Describes the downsampling method. Defaults to DownSampleType.AVG_POOLING.
            kernels (int, optional): Size of the convolutions kernels. Defaults to 3.
            first_kernel (int, optional): The first convolution can have a different kernel size, to e.g. increase the
                perceptive field, while the channel depth is still low. Defaults to 5.
            split_kernels (bool, optional): To decrease the number of parameters, a convolution with the kernel_size
                `(kernel,kernel)` can be splitted into two consecutive convolutions with the kernel_size `(kernel,1)` and
                `(1,kernel)` respectivly. Defaults to False.
            number_of_blocks (int, optional): Number of consecutive convolutional building blocks, i.e. `Conv2DBlock`.
                Defaults to 2.
            activation (str, optional): String literal or tensorflow activation function object to obtain activation
                function. Defaults to "leaky_relu".
            use_ResidualBlock (bool, optional): Whether or not to use the ResidualBlock instead of the
                `Conv2DBlock`. Defaults to False.
            residual_cardinality (int, optional): Cardinality for the `ResidualBlock`. Defaults to 1.
            limit_filters (int, optional): Limits the number of filters, which is doubled with every downsampling block.
                Defaults to 512.
            n_bottleneck_blocks (int, optional): Number of consecutive convolution blocks in the bottleneck. Defaults to 1.
            filters (int, optional): Number of filters for the initial encoder block. Defaults to 64.
            dropout_rate (float, optional): Probability of the dropout layer. If the preceeding layer has more than one
                channel, spatial dropout is applied, otherwise standard dropout. Defaults to 0.2.
            use_self_attention (bool, optional): Determines whether to apply self-attention in the decoder. Defaults to
                False.
            use_spec_norm (bool, optional): Applies spectral normalization to convolutional and dense layers. Defaults to
                False.
            use_bias (bool, optional): Whether convolutions and dense layers include a bias or not. Defaults to True.
            linear_layer_type (LinearLayerType, optional): Determines whether 1x1 convolutions are replaced by linear
                layers, which gives the same result, but linear layers are faster. Option: LinearLayerType.MLP or
                LinearLayerType.CONV_1x1. Defaults to LinearLayerType.MLP.
            padding (PaddingType, optional): Padding type. Defaults to PaddingType.ZERO.
            kernel_initializer (tf.keras.initializers.Initializer, optional): Initialization of the convolutions kernels.
                Defaults to None.
            gamma_initializer (tf.keras.initializers.Initializer, optional): Initialization of the normalization layers.
                Defaults to None.
        """
        super(UNetDiscriminator, self).__init__()
        ch = filters

        self.input_spec = tf.keras.layers.InputSpec(ndim=4)

        self.encoder = Encoder(number_of_levels=number_of_levels, filters=filters, limit_filters=limit_filters,  downsampling=downsampling, kernels=kernels, split_kernels=split_kernels, number_of_blocks=number_of_blocks,activation=activation, first_kernel=first_kernel, use_ResidualBlock=use_ResidualBlock, channel_list=[ch,2*ch,4*ch,8*ch,8*ch], use_spec_norm=use_spec_norm,use_self_attention=use_self_attention,output_skips=True, use_bias = use_bias,residual_cardinality=residual_cardinality,padding = padding, kernel_initializer = kernel_initializer, gamma_initializer = gamma_initializer)
        self.bottleNeck = Bottleneck(use_ResidualBlock=use_ResidualBlock, n_bottleneck_blocks=n_bottleneck_blocks, kernels=kernels, split_kernels=split_kernels,number_of_blocks=number_of_blocks, activation = activation,dropout_rate=dropout_rate, channel_list=[16*ch], use_spec_norm=use_spec_norm, use_bias = use_bias,residual_cardinality=residual_cardinality,padding = padding, kernel_initializer = kernel_initializer, gamma_initializer = gamma_initializer)
        self.decoder = Decoder(number_of_levels=number_of_levels, upsampling=upsampling, filters=filters, limit_filters=limit_filters, kernels=kernels, split_kernels=split_kernels,number_of_blocks=number_of_blocks,activation=activation,dropout_rate=dropout_rate, use_ResidualBlock=use_ResidualBlock, channel_list=[8*ch,8*ch,4*ch,2*ch,ch], use_spec_norm=use_spec_norm, use_bias = use_bias,residual_cardinality=residual_cardinality,padding = padding, kernel_initializer = kernel_initializer, gamma_initializer = gamma_initializer,enable_skip_connections_input=True)
        if linear_layer_type == LinearLayerType.MLP:
            self.img_reconstruction = DenseBlock(units = 1, use_spec_norm = use_spec_norm, number_of_blocks = 1, activation = None, apply_final_normalization = False, use_bias = use_bias, kernel_initializer = kernel_initializer, gamma_initializer = gamma_initializer)
        elif linear_layer_type == LinearLayerType.CONV_1x1:
            self.img_reconstruction = Conv2DBlock(filters = 1,  kernels = 1, split_kernels  = False, number_of_blocks = 1, activation = None,use_spec_norm=use_spec_norm, apply_final_normalization = False, use_bias = use_bias,padding = padding, kernel_initializer = kernel_initializer, gamma_initializer = gamma_initializer)
        self.linear = DenseBlock(units = 1, use_spec_norm = use_spec_norm, number_of_blocks = 1, activation = None, apply_final_normalization = False, use_bias = use_bias, kernel_initializer = kernel_initializer, gamma_initializer = gamma_initializer)
        #To enable mixed precission support for matplotlib and distributed training and to increase training stability
        self.linear_dtype = tf.keras.layers.Activation("linear", dtype = tf.float32)


    def call(self, inputs:tf.Tensor)->Tuple[tf.Tensor,tf.Tensor]:
        """Calls the `UNetDiscriminator` model.

        Args:
            inputs (tf.Tensor): Tensor of shape (`batch`,`height`,`width`,`channel`).

        Returns:
            decoder_output: Real/fake prediction for each pixel of shape (batch, height, width, 1)
            encoder_output: Global real/fake prediction of shape (batch, 1).
        """
        x = inputs
        encoder_output, skip_connections = self.encoder(x)
        bottleneck_output = self.bottleNeck(encoder_output)
        decoder_output = self.decoder([bottleneck_output,skip_connections])

        out1 = GlobalSumPooling2D()(bottleneck_output)
        out1 = self.linear(out1)
        out1 = self.linear_dtype(out1)

        out2 = self.img_reconstruction(decoder_output)
        out2 = self.linear_dtype(out2)
        return out1, out2
