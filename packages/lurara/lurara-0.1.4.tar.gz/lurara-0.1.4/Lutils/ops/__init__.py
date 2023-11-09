import numpy as np
import tensorflow as tf
from keras.layers import *
from keras import layers as _L, Sequential
from keras import Model, Input
from Lutils._basic import *
from Lutils.act import SILU
from Lutils.ops.conv import Conv2DBS, Conv1DBS
from Lutils.ops.sample import UCC2D, DCCC2D, UCC1D, DCCC1D



# 定义ConcatAny类
class ConcatA(Layer):
    """
    下面的输入都是可以被拼接起来的:
    shapes: (15,12) (15, 20) -> (15,20) (15, 20) -> concat
    shapes:  (12, 15) (10, 10) -> (12,15) (12, 15) -> concat
    """
    # 初始化函数
    def __init__(self, filters=None, padding="same", **kwargs):
        # 调用父类的初始化函数
        super(ConcatA, self).__init__(**kwargs)
        self.filters = filters
        self.padding = padding

    # 前向传播函数
    def call(self, list_inputs:list, axis=0, fill=0):
        # 获取输入的形状
        shapes = [tf.shape(input) for input in list_inputs]
        # 获取最大的形状
        max_shape = tf.reduce_max(tf.stack(shapes), axis=0)
        # 对每个输入进行填充
        padded_inputs = []
        for input in list_inputs:
            input_shape = tf.shape(input)
            paddings = tf.stack([tf.zeros_like(input_shape), max_shape - input_shape], axis=1)
            padded_input = tf.pad(input, paddings, constant_values=fill)
            padded_inputs.append(padded_input)
        # 拼接填充后的输入
        x = tf.concat(padded_inputs, axis=axis)

        if self.filters is None:
            return x

        x =  Conv2D(self.filters, 1, strides=1, padding=self.padding)(x)
        return x

# 定义类
class DimensionUp(Layer):
    # 初始化函数
    def __init__(self, input_shape=None, **kwargs):
        # 调用父类的初始化函数
        super(DimensionUp, self).__init__(**kwargs)
        self._input_shape = input_shape

    def call(self, inputs, *args, **kwargs):
        _new_shape = (*inputs.shape[1:], 1)
        return Reshape(_new_shape, input_shape=self._input_shape)(inputs)

class DimensionDown(Layer):
    # 初始化函数
    def __init__(self, input_shape=None, **kwargs):
        # 调用父类的初始化函数
        super(DimensionDown, self).__init__(**kwargs)
        self._input_shape = input_shape

    def call(self, inputs, *args, **kwargs):
        assert inputs.shape[-1] == 1, f"inputs.shape[-1] must be 1, but got {inputs.shape[-1]}"
        _new_shape = inputs.shape[1:-1]
        return Reshape(_new_shape, input_shape=self._input_shape)(inputs)

class WithDimensionUp(Layer):
    # 初始化函数
    def __init__(self, layer, input_shape=None, **kwargs):
        # 调用父类的初始化函数
        super(WithDimensionUp, self).__init__(**kwargs)
        self._input_shape = input_shape
        self.layer = layer

    def call(self, inputs, *args, **kwargs):
        _new_shape = (*inputs.shape[1:], 1)
        x = Reshape(_new_shape, input_shape=self._input_shape)(inputs)
        x = self.layer(x)
        assert x.shape[-1] == 1, f"x.shape[-1] must be 1, but got {inputs.shape[-1]}.This caused by your layer (which change the shape) to WithDimensionUp at initialize."
        _new_shape = x.shape[1:-1]
        return Reshape(_new_shape, input_shape=x.shape[1:])(x)

if  __name__ == '__main__':
    ...

