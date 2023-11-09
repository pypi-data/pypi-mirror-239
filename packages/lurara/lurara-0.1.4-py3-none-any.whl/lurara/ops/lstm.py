from keras.layers import *
from lurara.act import SILU


class LSTMBS:
    def __new__(cls, inputs, unit, sentences=False):
        x = LSTM(unit, return_sequences=sentences)(inputs)
        x = BatchNormalization()(x)
        x = SILU()(x)
        return x

