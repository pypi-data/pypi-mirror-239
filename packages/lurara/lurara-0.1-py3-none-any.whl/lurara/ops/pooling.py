from lurara.ops.conv import Conv2DBS, Conv1DBS
from keras.layers import Concatenate, MaxPool2D

class SPPF2D:
    def __new__(cls, inputs, filters):
        x0 = Conv2DBS.ReChannels(inputs, filters)
        x1 = MaxPool2D(2, 1, 'same')(x0)
        x2 = MaxPool2D(3, 1, 'same')(x1)
        x3 = MaxPool2D(4, 1, 'same')(x2)
        x = Concatenate(axis=-1)([x0, x1, x2, x3])
        x = Conv2DBS.ReChannels(x, filters)
        return x


class SPPF1D:
    def __new__(cls, inputs, filters):
        x0 = Conv1DBS.ReChannels(inputs, filters)
        x1 = MaxPool1D(2, 1, 'same')(x0)
        x2 = MaxPool1D(3, 1, 'same')(x1)
        x3 = MaxPool1D(4, 1, 'same')(x2)
        x = Concatenate(axis=-1)([x0, x1, x2, x3])
        x = Conv1DBS.ReChannels(x, filters)
        return x