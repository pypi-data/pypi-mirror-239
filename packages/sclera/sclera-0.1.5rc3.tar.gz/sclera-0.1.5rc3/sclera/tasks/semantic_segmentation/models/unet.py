import keras_core as keras


class UnetModule(keras.layers.Layer):
    def __init__(
        self, encoder_depth, decoder_depth, filters, activation="relu"
    ):
        super(UnetModule, self).__init__()

        self.encoder_layers = []
        for i in range(encoder_depth):
            self.encoder_layers.append(
                keras.layers.Conv2D(
                    filters, 3, activation=activation, padding="same"
                )
            )
            self.encoder_layers.append(keras.layers.BatchNormalization())
            self.encoder_layers.append(keras.layers.MaxPooling2D(2, 2))

        self.decoder_layers = []
        for i in range(decoder_depth):
            self.decoder_layers.append(
                keras.layers.Conv2DTranspose(
                    filters, 3, activation=activation, padding="same"
                )
            )
            self.decoder_layers.append(keras.layers.BatchNormalization())
            self.decoder_layers.append(keras.layers.UpSampling2D(2))

    def call(self, inputs):
        # Encoder
        encoder_outputs = []
        for layer in self.encoder_layers:
            encoder_outputs.append(layer(inputs))
            inputs = encoder_outputs[-1]

        # Decoder
        for i in range(len(self.decoder_layers) - 1, -1, -1):
            inputs = keras.layers.concatenate(
                [encoder_outputs[i], inputs], axis=-1
            )
            inputs = self.decoder_layers[i](inputs)

        return inputs


class UNet(keras.models.Model):
    """
    The U-Net model is a commonly-used Segmentation Network
    that consists of an U-shaped network.
    Args:
        depth: The depth of the encoder and decoder parts of the U-Net.
            The decoder depth must be equal to the encoder depth.
        filters: The number of filters to use in the first layer of the
            U-Net. The number of filters will be doubled after each
            max-pooling layer in the encoder part of the U-Net, and
            halved after each up-sampling layer in the decoder
            part of the U-Net.
        activation: The activation function to use in the U-Net.

    Example Usage:
        ```python
        input_shape = (256, 256, 3)
        depth = 5
        filters = 64
        activation='relu'

        model = Unet(depth=depth, filters=filters, activation=activation, input_shape=input_shape)
        ```
    """

    def __init__(
        self,
        depth,
        filters,
        input_shape=(224, 224, 3),
        activation="relu",
    ):
        super(UNet, self).__init__()

        # Modules
        self.modules = []
        for i in range(depth + depth):
            if i < depth:
                filters *= 2
            else:
                filters //= 2

            self.modules.append(UnetModule(1, 1, filters, activation))

        # Output
        self.output_layer = keras.layers.Conv2D(1, 1, activation="sigmoid")

    def call(self, inputs):
        x = inputs
        for module in self.modules:
            x = module(x)

        return self.output_layer(x)
