import keras_core as keras


class UnetModule(keras.Model):
    def __init__(
        self, encoder_depth, decoder_depth, filters, activation="relu"
    ):
        super().__init__()
        self.depth = decoder_depth
        self.width = 3 # Depends on the number of layers per block, paper has 3 

        self.encoder_layers = []
        for i in range(encoder_depth):
            self.encoder_layers.append(
                keras.layers.Conv2D(
                    filters, 3, activation=activation, padding="same"
                )
            )
            self.encoder_layers.append(keras.layers.BatchNormalization())
            self.encoder_layers.append(keras.layers.MaxPooling2D(2, 2))
            filters *= 2

        self.decoder_layers = []
        for i in range(decoder_depth):
            self.decoder_layers.append(
                keras.layers.Conv2DTranspose(
                    int(filters), 3, activation=activation, padding="same"
                )
            )
            self.decoder_layers.append(keras.layers.BatchNormalization())
            self.decoder_layers.append(keras.layers.UpSampling2D(2))
            filters /= 2

    def build(self, input_shape):
        super().build(input_shape=input_shape)

    def call(self, inputs):
        # Encoder
        encoder_outputs = []
        for idx, layer in enumerate(self.encoder_layers, 1):
            inputs = layer(inputs)
            if idx % 3 == 0:
                encoder_outputs.append(inputs)

        # Decoder
        for idx, layer in enumerate(self.decoder_layers, 1):
            if idx % 3 == 1:
                pos = len(encoder_outputs) - (idx // self.width) - 1
                inputs = keras.layers.Concatenate()([encoder_outputs[pos], inputs])
            inputs = layer(inputs)

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
        depth = 5
        filters = 64
        activation='relu'
        input_shape = (256, 256, 3)

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

        # Modules
        inputs = keras.layers.Input(shape=input_shape)
        x = inputs

        x = UnetModule(depth, depth, filters, activation)(x)

        # Output
        output_layer = keras.layers.Conv2D(1, 1, activation="sigmoid")(x)

        super().__init__(inputs=inputs, outputs=output_layer)
