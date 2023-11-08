from Lutils._basic import *
from Lutils.act import *
from keras.layers import *
from keras import Model, Input
import tensorflow as tf


# Conv2D with BatchNormalization and SILU
class Conv2DBS:
    """
    (n, 1, 1, a) -> (n, 1 / strides, 1 / strides, filters)  # In Same Case
    基础的Conv2D with BatchNormalization and SILU结构
    BatchNormalization用于差异化明显的数据, 可降低这种差异带来的影响
    SILU用于非线性激活, 加速收敛, 且不改变输入的分布. 曲线和ReLU相似, 且比ReLU更快, 不会出现ReLU的梯度消失问题.
    """
    def __new__(cls, inputs, filters, kernel_size, strides, padding="same") -> tf.Tensor:
        x = Conv2D(filters, kernel_size, strides=strides, padding=padding, use_bias=False)(inputs)
        x = BatchNormalization()(x)
        x = SILU()(x)
        return x

    @staticmethod
    def TakeFeatures(inputs, filters) -> tf.Tensor:
        """
        (n, 1, 1, a) -> (n, .5, .5, filters)
        用于提取特征的ConvBS, 即
        ConvBS(inputs, filters, 3, 2)
        :param inputs:
        :param filters:
        :return:
        """
        x = Conv2DBS(inputs, filters, 3, 2)
        return x

    @staticmethod
    def ReChannels(inputs, filters) -> tf.Tensor:
        """
        (n, 1, 1, a) -> (n, 1, 1, filters)
        用于改变通道数的ConvBS, 即
        ConvBS(inputs, filters, 1, 1, 'valid')
        :param inputs:
        :param filters:
        :return:
        """
        x = Conv2DBS(inputs, filters, 1, 1, 'valid')
        return x

    @staticmethod
    def DarkBottle(inputs, filters, add=False) -> tf.Tensor:
        """
        (n, 1, 1, a) -> (n, 1, 1, filters)
        用于特征重整,并且可以缓减梯度消失问题
        ...
        :param inputs:
        :param filters:
        :param add: 前后add,缓减梯度消失. 但会影响神经元数据输出值
        :return:
        """
        x = Conv2DBS(inputs, filters // 2, 3, 1, padding='same')
        x = Conv2DBS(x, filters, 3, 1, padding='same')
        if add:
            return tf.add(x, inputs)
        return x

    @staticmethod
    def CSPConvB(inputs, filters, splits:int=2, add=False):
        """
        (n, 1, 1, a) -> (n, 1, 1, filters)
        用于特征重整和筛选,并且可以缓减梯度消失问题
        :param inputs:
        :param filters:
        :param splits:
        :param add: 前后add,缓减梯度消失. 但会影响神经元数据输出值
        :return:
        """
        assert isinstance(splits, int) and splits >= 1, 'splits must be integer and >= 1'
        x = Conv2DBS.ReChannels(inputs, filters)
        if splits == 1:
            xs = [x]
        else:
            xs = tf.split(x, splits, axis=-1)
        for i in range(splits):
            xs[i] = Conv2DBS.DarkBottle(xs[i], filters // splits, add=add)
        x = tf.concat([x] + xs, axis=-1)
        return Conv2DBS.ReChannels(x, filters)

    @staticmethod
    def CCUnit(inputs, filters, splits:int=2):
        """
        (n, 1, 1, a) -> (n, 1, 1, filters)
        用于特征重整和筛选,并且可以缓减梯度消失问题
        :param inputs:
        :param filters:
        :param splits:
        :return:
        """
        x = Conv2DBS.TakeFeatures(inputs, filters)
        x = Conv2DBS.CSPConvB(x, filters, splits=int(splits + .5), add=True)
        return x

# Conv1D with BatchNormalization and SILU
class Conv1DBS:
    """
    (n, 1, a) -> (n, 1 / strides, filters)  # In Same Case
    基础的Conv1D with BatchNormalization and SILU结构
    BatchNormalization用于差异化明显的数据, 可降低这种差异带来的影响
    SILU用于非线性激活, 加速收敛, 且不改变输入的分布. 曲线和ReLU相似, 且比ReLU更快, 不会出现ReLU的梯度消失问题.
    """
    def __new__(cls, inputs, filters, kernel_size, strides, padding="same") -> tf.Tensor:
        x = Conv1D(filters, kernel_size, strides=strides, padding=padding, use_bias=False)(inputs)
        x = BatchNormalization()(x)
        x = SILU()(x)
        return x

    @staticmethod
    def TakeFeatures(inputs, filters) -> tf.Tensor:
        """
        (n, 1, a) -> (n, .5, filters)
        用于提取特征的ConvBS, 即
        Conv1DBS(inputs, filters, 3, 2)
        :param inputs:
        :param filters:
        :return:
        """
        x = Conv1DBS(inputs, filters, 3, 2)
        return x

    @staticmethod
    def ReChannels(inputs, filters) -> tf.Tensor:
        """
        (n, 1, a) -> (n, 1, filters)
        用于改变通道数的Conv1DBS, 即
        Conv1DBS(inputs, filters, 1, 1, 'valid')
        :param inputs:
        :param filters:
        :return:
        """
        x = Conv1DBS(inputs, filters, 1, 1, 'valid')
        return x

    @staticmethod
    def DarkBottle(inputs, filters, add=False) -> tf.Tensor:
        """
        (n, 1, a) -> (n, 1, filters)
        用于特征重整,并且可以缓减梯度消失问题
        ...
        :param inputs:
        :param filters:
        :param add: 前后add,缓减梯度消失. 但会影响神经元数据输出值
        :return:
        """
        x = Conv1DBS(inputs, filters // 2, 3, 1, padding='same')
        x = Conv1DBS(x, filters, 3, 1, padding='same')
        if add:
            return tf.add(x, inputs)
        return x

    @staticmethod
    def CSPConvB(inputs, filters, splits:int=2, add=False):
        """
        (n, 1, a) -> (n, 1, filters)
        用于特征重整和筛选,并且可以缓减梯度消失问题
        :param inputs:
        :param filters:
        :param splits:
        :param add: 前后add,缓减梯度消失. 但会影响神经元数据输出值
        :return:
        """
        assert isinstance(splits, int) and splits > 1, 'splits must be integer and > 1'
        x = Conv1DBS.ReChannels(inputs, filters)
        xs = tf.split(x, splits, axis=-1)
        for i in range(splits):
            xs[i] = Conv1DBS.DarkBottle(xs[i], filters // splits, add=add)
        x = tf.concat([x] + xs, axis=-1)
        return Conv1DBS.ReChannels(x, filters)

    @staticmethod
    def CCUnit(inputs, filters, splits:int=2):
        """
        (n, 1, a) -> (n, 1, filters)
        用于特征重整和筛选,并且可以缓减梯度消失问题
        :param inputs:
        :param filters:
        :param splits:
        :return:
        """
        x = Conv1DBS.TakeFeatures(inputs, filters)
        x = Conv1DBS.CSPConvB(x, filters, splits=int(splits), add=True)
        return x


if  __name__ == "__main__":
    inputs = Input(shape=(224, 224, 3))
    x = Conv2DBS.TakeFeatures(inputs, 16)
    print(x)

