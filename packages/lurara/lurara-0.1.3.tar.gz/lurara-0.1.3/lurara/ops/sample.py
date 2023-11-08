from lurara._basic import *
from lurara.act import *
from keras.layers import *
from keras import Model, Input
import tensorflow as tf

from lurara.ops.conv import Conv2DBS, Conv1DBS


class UCC2D:
    def __new__(cls, shallow_inputs, deep_inputs) -> tf.Tensor:
        """
        (n, 1, 1, a2), (n, 2, 2, a1) -> (n, 2, 2, a1)
        * a2 > a1 . gernaerally.
        :param shallow_inputs: (n, 2, 2, a1)
        :param deep_inputs: (n, 1, 1, a2)
        :return: (n, 2, 2, a1)
        """
        shallow_x = UpSampling2D()(deep_inputs)
        x = tf.concat([shallow_inputs, shallow_x], axis=-1)
        x = Conv2DBS.CSPConvB(x, shallow_inputs.shape[-1], add=False)
        return x


class DCCC2D:
    def __new__(cls, shallow_inputs, deep_inputs) -> tf.Tensor:
        """
        (n, 1, 1, a2), (n, 2, 2, a1) -> (n, 1, 1, a2)
        * a2 > a1 . gernaerally.
        :param shallow_inputs: (n, 2, 2, a1)
        :param deep_inputs: (n, 1, 1, a2)
        :return: (n, 2, 2, a1)
        """
        deep_x = Conv2DBS.TakeFeatures(shallow_inputs, deep_inputs.shape[-1])
        x = tf.concat([deep_inputs, deep_x], axis=-1)
        x = Conv2DBS.CSPConvB(x, deep_inputs.shape[-1], add=False)
        return x

class UCC1D:
    def __new__(cls, shallow_inputs, deep_inputs) -> tf.Tensor:
        """
        (n, 1, a2), (n, 2, a1) -> (n, 2, a1)
        * a2 > a1 . gernaerally.
        :param shallow_inputs: (n, 2, a1)
        :param deep_inputs: (n, 1, a2)
        :return: (n, 2, a1)
        """
        shallow_x = UpSampling1D()(deep_inputs)
        x = tf.concat([shallow_inputs, shallow_x], axis=-1)
        x = Conv1DBS.CSPConvB(x, shallow_inputs.shape[-1], add=False)
        return x


class DCCC1D:
    def __new__(cls, shallow_inputs, deep_inputs) -> tf.Tensor:
        """
        (n, 1, a2), (n, 2, a1) -> (n, 1, a2)
        * a2 > a1 . gernaerally.
        :param shallow_inputs: (n, 2, a1)
        :param deep_inputs: (n, 1, a2)
        :return: (n, 2, a1)
        """
        deep_x = Conv1DBS.TakeFeatures(shallow_inputs, deep_inputs.shape[-1])
        x = tf.concat([deep_inputs, deep_x], axis=-1)
        x = Conv1DBS.CSPConvB(x, deep_inputs.shape[-1], add=False)
        return x

