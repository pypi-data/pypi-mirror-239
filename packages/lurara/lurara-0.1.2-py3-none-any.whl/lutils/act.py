# -*- coding: utf-8 -*-
from keras import layers as _L
from keras import Input
from Lutils._basic import *
import tensorflow as tf


# 定义Sigmoid类，继承自_L.Layer
class Sigmoid(_L.Layer):
    """
    Sigmoid(x) = 1 / (1 + exp(-x))，它的输出范围是(0, 1)，具有指数形状，可以表示为概率或者用于输入的归一化。它的缺点是容易出现饱和和梯度消失，以及输出不是零均值的。
    """

    # 初始化方法，接收一个name参数，表示层的名称
    def __init__(self, name=None):
        # 调用父类的初始化方法
        super(Sigmoid, self).__init__(name=name)

    # 前向传播方法，接收一个inputs参数，表示输入张量
    def call(self, inputs):
        # 使用tensorflow的sigmoid函数直接计算激活函数的值，并返回结果
        return tf.math.sigmoid(inputs)


# 定义Tanh类，继承自_L.Layer
class Tanh(_L.Layer):
    """
    Tanh(x) = (exp(x) - exp(-x)) / (exp(x) + exp(-x))，它的输出范围是(-1, 1)，是零均值的，比Sigmoid函数收敛速度更快。它的缺点也是容易出现饱和和梯度消失。
    """

    # 初始化方法，接收一个name参数，表示层的名称
    def __init__(self, name=None):
        # 调用父类的初始化方法
        super(Tanh, self).__init__(name=name)

    # 前向传播方法，接收一个inputs参数，表示输入张量
    def call(self, inputs):
        # 使用tensorflow的tanh函数直接计算激活函数的值，并返回结果
        return tf.math.tanh(inputs)


# 定义ReLU类，继承自_L.Layer
class ReLU(_L.Layer):
    """
    ReLU(x) = max(0, x)，它的输出范围是[0, +∞)，具有线性和非线性的特点，可以缓解梯度消失问题，训练速度快。它的缺点是当输入为负时，输出为零，导致部分神经元死亡，以及输出不是零均值的。
    """

    # 初始化方法，接收一个name参数，表示层的名称
    def __init__(self, name=None):
        # 调用父类的初始化方法
        super(ReLU, self).__init__(name=name)

    # 前向传播方法，接收一个inputs参数，表示输入张量
    def call(self, inputs):
        # 使用tensorflow的relu函数直接计算激活函数的值，并返回结果
        return tf.nn.relu(inputs)


# 定义LeakyReLU类，继承自_L.Layer
class LeakyReLU(_L.Layer):
    """
    Leaky ReLU(x) = max(αx, x)，其中α是一个很小的常数，例如0.01。它是为了解决ReLU函数在负区域导致神经元死亡的问题，让负区域有一个很小的梯度。它的优点是保留了ReLU函数的优势，缺点是输出仍然不是零均值的。
    """

    # 初始化方法，接收一个alpha参数，表示负区域的斜率系数，默认为0.01；和一个name参数，表示层的名称
    def __init__(self, alpha=0.01, name=None):
        # 调用父类的初始化方法
        super(LeakyReLU, self).__init__(name=name)
        # 保存alpha参数为一个属性
        self.alpha = alpha

    # 前向传播方法，接收一个inputs参数，表示输入张量
    def call(self, inputs):
        # 使用tensorflow的leaky_relu函数直接计算激活函数的值，并返回结果
        return tf.nn.leaky_relu(inputs, alpha=self.alpha)


# 定义PReLU类，继承自_L.Layer
class PReLU(_L.Layer):
    """
    PReLU(x) = max(αx, x)，其中α是一个可学习的参数，可以通过反向传播进行更新。它是Leaky ReLU函数的一种改进，可以自适应地调整负区域的梯度。它在某些任务上表现得比ReLU函数更好，但也更容易过拟合。
    """

    # 初始化方法，接收一个name参数，表示层的名称
    def __init__(self, name=None):
        # 调用父类的初始化方法
        super(PReLU, self).__init__(name=name)
        # 定义一个可学习的参数alpha，初始值为0.25，范围为[0, 1]
        self.alpha = self.add_weight(name='alpha', shape=(), initializer='constant', trainable=True,
                                     constraint=keras.constraints.min_max_norm(min_value=0, max_value=1),
                                     dtype=tf.float32, default_value=0.25)

    # 前向传播方法，接收一个inputs参数，表示输入张量
    def call(self, inputs):
        # 使用tensorflow的maximum函数和multiply函数直接计算激活函数的值，并返回结果
        return tf.maximum(self.alpha * inputs, inputs)


# 定义ReLU6类，继承自_L.Layer
class ReLU6(_L.Layer):
    """
    ReLU6(x) = min(max(0, x), 6)，它是ReLU函数的一种变体，限制了输出范围在[0, 6]之间。它主要用于移动端设备上的低精度计算，以保证数值分辨率。它相比于ReLU函数有更好的饱和性，但也损失了一些表达能力。
    """

    # 初始化方法，接收一个name参数，表示层的名称
    def __init__(self, name=None):
        # 调用父类的初始化方法
        super(ReLU6, self).__init__(name=name)

    # 前向传播方法，接收一个inputs参数，表示输入张量
    def call(self, inputs):
        # 使用tensorflow的relu6函数直接计算激活函数的值，并返回结果
        return tf.nn.relu6(inputs)


# 定义Softsign类，继承自_L.Layer
class Softsign(_L.Layer):
    """
    Softsign(x) = x / (1 + |x|)，它是Tanh函数的一种替代选择，具有类似的曲线形状和输出范围。它相比于Tanh函数更平滑，导数下降更慢，可以缓解梯度消失问题。
    """

    # 初始化方法，接收一个name参数，表示层的名称
    def __init__(self, name=None):
        # 调用父类的初始化方法
        super(Softsign, self).__init__(name=name)

    # 前向传播方法，接收一个inputs参数，表示输入张量
    def call(self, inputs):
        # 使用tensorflow的softsign函数直接计算激活函数的值，并返回结果
        return tf.nn.softsign(inputs)


# 定义Softplus类，继承自_L.Layer
class Softplus(_L.Layer):
    """
    Softplus(x) = log(1 + exp(x))，它是ReLU函数的一种替代选择，具有类似的曲线形状和输出范围。它相比于ReLU函数更光滑，导数连续且非零，可以防止神经元死亡。它的缺点是不对称，不以零为中心，可能出现梯度消失的问题。
    """

    # 初始化方法，接收一个name参数，表示层的名称
    def __init__(self, name=None):
        # 调用父类的初始化方法
        super(Softplus, self).__init__(name=name)

    # 前向传播方法，接收一个inputs参数，表示输入张量
    def call(self, inputs):
        # 使用tensorflow的softplus函数直接计算激活函数的值，并返回结果
        return tf.nn.softplus(inputs)


# 定义ELU类，继承自_L.Layer
class ELU(_L.Layer):
    """
    ELU(x) = x, if x > 0; α(exp(x) - 1), if x ≤ 0，其中α是一个常数，例如1。它是一种结合了Sigmoid和ReLU函数特点的激活函数，左侧具有软饱和性，右侧无饱和性。它可以缓解梯度消失问题，对输入变化或噪声更鲁棒，输出接近于零均值，收敛速度快。它的缺点是计算量相对较大。
    """
    # 前向传播方法，接收一个inputs参数，表示输入张量
    def call(self, inputs):
        # 使用tensorflow的elu函数直接计算激活函数的值，并返回结果
        return tf.nn.elu(inputs)


# 定义SELU类，继承自_L.Layer
class SELU(_L.Layer):
    """
    SELU(x) = λx, if x > 0; λα(exp(x) - 1), if x ≤ 0，其中λ和α是常数，例如1.0507和1.6733。它是ELU函数的一种改进，可以使得输入在经过多层之后保持一个固定的分布，从而提高网络的稳定性和收敛性。它的缺点是需要对输入进行标准化处理，以及对网络结构有一定的限制。
    """
    # 初始化方法，接收一个name参数，表示层的名称
    def __init__(self, name=None):
        # 调用父类的初始化方法
        super(SELU, self).__init__(name=name)
        # 定义两个常数lambda和alpha，用于计算激活函数的值
        self.lambd = 1.0507009873554804934193349852946
        self.alpha = 1.6732632423543772848170429916717

    # 前向传播方法，接收一个inputs参数，表示输入张量
    def call(self, inputs):
        # 使用tensorflow的selu函数直接计算激活函数的值，并返回结果
        return tf.nn.selu(inputs)

# 定义SILU类，继承自_L.Layer
class SILU(_L.Layer):
    """
    SILU(x) = x * sigmoid(x)，其中sigmoid(x) = 1 / (1 + exp(-x))。它是一种结合了线性和非线性特性的激活函数，可以保留输入的信息，避免信息损失，同时也提高模型的表达能力。它可以实现自稳定，使得神经网络的隐藏层在训练过程中保持输出的均值和方差接近于1，从而提高网络的稳定性和收敛性。它可以近似任意凸函数，可以避免梯度消失和爆炸问题，可以提高神经网络的鲁棒性和容错性。
    """

    # 初始化函数
    def __init__(self):
        # 调用父类的初始化函数
        super(SILU, self).__init__()

    # 前向传播函数，输入为x
    def call(self, x):
        # 返回x乘以sigmoid(x)
        return x * tf.math.sigmoid(x)


# 定义GELU类，继承自_L.Layer
class GELU(_L.Layer):
    """
    GELU(x) = x * Φ(x)，其中Φ(x)是标准正态分布的累积分布函数。它是一种近似于ReLU函数的激活函数，具有平滑和非单调的特性，可以提高神经网络的表达能力和泛化能力
    """

    # 前向传播方法，接收一个inputs参数，表示输入张量
    def call(self, inputs):
        # 使用tensorflow的gelu函数直接计算激活函数的值，并返回结果
        return tf.nn.gelu(inputs)


# 定义Swish类，继承自_L.Layer
class Swish(_L.Layer):
    """
    Swish(x) = x * sigmoid(βx)，其中β是一个可学习的参数或一个固定的常数。它是一种自门控的激活函数，可以根据输入自适应地调整信息流的量，可以提高神经网络的准确率和收敛速度
    """

    # 初始化方法，接收一个beta参数，表示sigmoid函数的系数，默认为1.0；和一个name参数，表示层的名称
    def __init__(self, beta=1.0, name=None):
        # 调用父类的初始化方法
        super(Swish, self).__init__(name=name)
        # 保存beta参数为一个属性
        self.beta = beta

    # 前向传播方法，接收一个inputs参数，表示输入张量
    def call(self, inputs):
        # 使用tensorflow的sigmoid函数和multiply函数直接计算激活函数的值，并返回结果
        return tf.multiply(inputs, tf.math.sigmoid(self.beta * inputs))


# 定义Maxout类，继承自_L.Layer
class Maxout(_L.Layer):
    """
    Maxout(x) = max(w1x + b1, w2x + b2)，其中w1, w2, b1, b2是可学习的参数。它是一种分段线性的激活函数，可以近似任意凸函数，可以避免梯度消失和爆炸问题，可以提高神经网络的鲁棒性和容错性 。
    """

    # 初始化方法，接收一个units参数，表示输出张量的最后一维的大小；和一个name参数，表示层的名称
    def __init__(self, units, name=None):
        # 调用父类的初始化方法
        super(Maxout, self).__init__(name=name)
        # 保存units参数为一个属性
        self.units = units
        # 定义两个可学习的参数w1和w2，形状为(输入张量的最后一维大小, units)，初始值为随机正态分布
        self.w1 = self.add_weight(name='w1', shape=(None, units), initializer='random_normal', trainable=True)
        self.w2 = self.add_weight(name='w2', shape=(None, units), initializer='random_normal', trainable=True)
        # 定义两个可学习的参数b1和b2，形状为(units,)，初始值为0
        self.b1 = self.add_weight(name='b1', shape=(units,), initializer='zeros', trainable=True)
        self.b2 = self.add_weight(name='b2', shape=(units,), initializer='zeros', trainable=True)

    # 前向传播方法，接收一个inputs参数，表示输入张量
    def call(self, inputs):
        # 使用tensorflow的matmul函数和add函数计算两个线性变换的结果
        z1 = tf.add(tf.matmul(inputs, self.w1), self.b1)
        z2 = tf.add(tf.matmul(inputs, self.w2), self.b2)
        # 使用tensorflow的maximum函数直接计算激活函数的值，并返回结果
        return tf.maximum(z1, z2)


class Mish(_L.Layer):
    """
    Mish(x) = x * tanh(softplus(x))，其中softplus(x) = log(1 + exp(x))。它是一种自门控的激活函数，可以根据输入自适应地调整信息流的量，可以提高神经网络的准确率和收敛速度。它具有平滑和非单调的特性，可以提高神经网络的表达能力和泛化能力。它可以避免梯度消失和爆炸问题，可以提高神经网络的鲁棒性和容错性。
    """
    def __init__(self, name=None):
        super(Mish, self).__init__(name=name)

    def call(self, inputs):
        return inputs * tf.math.tanh(tf.math.softplus(inputs))


class Hardtanh(_L.Layer):
    """
    Hardtanh(x) = max(-1, min(1, x))，它是Tanh函数的一种变体，限制了输出范围在[-1, 1]之间。它主要用于低精度计算，以保证数值分辨率。它相比于Tanh函数有更好的饱和性，但也损失了一些表达能力。
    """
    def __init__(self, name=None):
        super(Hardtanh, self).__init__(name=name)

    def call(self, inputs):
        return tf.clip_by_value(inputs, -1, 1)


class ArcTan(_L.Layer):
    """
    ArcTan(x) = arctan(x)，它是一种反三角函数，具有类似于Tanh函数的曲线形状和输出范围。它相比于Tanh函数更平滑，导数下降更慢，可以缓解梯度消失问题。
    """
    def __init__(self, name=None):
        super(ArcTan, self).__init__(name=name)

    def call(self, inputs):
        return tf.math.atan(inputs)


# 定义RReLU类，继承自_L.Layer
class RReLU(_L.Layer):
    """
    RReLU是ReLU的一种变体，它在训练期间为负输入选择一个随机斜率，在测试期间使用平均斜率。这种方法有助于防止过拟合。
    """
    def __init__(self, alpha=0.1, name=None):
        super(RReLU, self).__init__(name=name)
        self.alpha = alpha

    def call(self, inputs):
        return tf.maximum(0., inputs) + self.alpha * tf.minimum(0., inputs)

# 定义Softmax类，继承自_L.Layer
class Softmax(_L.Layer):
    """
    Softmax函数用于多类分类问题，它将输出层的值通过激活函数映射到0-1区间，构造成概率分布。Softmax激活函数映射值越大，则真实类别可能性越大。
    """
    def call(self, inputs):
        return tf.nn.softmax(inputs)

# 定义Softmin类，继承自_L.Layer
class Softmin(_L.Layer):
    """
    Softmin函数是Softmax函数的一个变体，它对输入向量的每个元素应用负指数，然后对结果进行归一化。这样可以将任意长度的实向量压缩到0-1之间，并且向量中元素的总和为1。
    """
    def call(self, inputs):
        return tf.nn.softmin(inputs)

# 定义Softshrink类，继承自_L.Layer
class Softshrink(_L.Layer):
    """
    Softshrink是一种非线性激活函数，当输入值大于某个阈值时，输出为x-threshold；当输入值小于负阈值时，输出为x+threshold；否则输出为0。
    """
    def __init__(self, lambda_=0.5, name=None):
        super(Softshrink, self).__init__(name=name)
        self.lambda_ = lambda_

    def call(self, inputs):
        return tf.where(tf.abs(inputs) - self.lambda_ < 0, 0., inputs)

# 定义Hardshrink类，继承自_L.Layer
class Hardshrink(_L.Layer):
    """
    Hardshrink是一种非线性激活函数，它在输入值大于某个阈值时输出原始值，在输入值小于负阈值时也输出原始值，否则输出0。这种硬缩减操作可以帮助模型学习具有稀疏性的表示，有助于减少模型的计算复杂性和参数数量。
    """
    def __init__(self, lambda_=0.5, name=None):
        super(Hardshrink, self).__init__(name=name)
        self.lambda_ = lambda_

    def call(self, inputs):
        return tf.where(tf.abs(inputs) > self.lambda_, inputs, 0.)

# 定义Tanhshrink类，继承自_L.Layer
class Tanhshrink(_L.Layer):
    """
    Tanhshrink函数计算输入和tanh函数之间的差值，即x - tanh(x)。
    """
    def call(self, inputs):
        return inputs - tf.math.tanh(inputs)

# 定义Threshold类，继承自_L.Layer
class Threshold(_L.Layer):
    """
    Threshold（阈值）激活函数是一种最简单的非线性激活函数，它在神经网络中用于引入非线性性质。这种激活函数在输入大于某个阈值时输出1，否则输出0。简单来说，它模拟了一个开关的行为，输入超过阈值时激活（输出1），否则不激活（输出0）。
    """
    def __init__(self, threshold=1.0, value=0.0, name=None):
        super(Threshold, self).__init__(name=name)
        self.threshold = threshold
        self.value = value

    def call(self, inputs):
        return tf.where(inputs > self.threshold, inputs, self.value)

# 定义Hardswish类，继承自_L.Layer
class Hardswish(_L.Layer):
    """
    Hardswish是Swish激活函数的一种变体，它在输入值大于某个阈值或小于负阈值时输出原始值，否则输出的是输入值与（输入值+3）/6的乘积。这种硬编码的Swish只有在深层网络中才能发挥作。
    """
    def call(self, inputs):
        return inputs * tf.nn.relu6(inputs + 3.) / 6.

# 定义LogSigmoid类，继承自_L.Layer
class LogSigmoid(_L.Layer):
    """
    LogSigmoid激活函数是对Sigmoid函数求对数后得到的结果。它将输入的每个元素值x求以自然常数e为底的指数，然后再分别除以他们的和，最后取对数。
    """

    def call(self, inputs):
        return -tf.math.softplus(-inputs)

# 定义Hardsigmoid类，继承自_L.Layer
class Hardsigmoid(_L.Layer):
    """
    Hardsigmoid是一种近似于Sigmoid函数的非线性激活函数。它在输入值大于某个阈值或小于负阈值时输出原始值，否则输出的是输入值/6 + 1/2。
    """
    def call(self, inputs):
        return tf.nn.relu6(inputs + 3.) / 6.

# 定义Softmax2d类，继承自_L.Layer
class Softmax2d(_L.Layer):
    """
    Softmax2D激活函数是对二维矩阵（或张量）的操作，类似于一维数据中的Softmax激活函数，但是应用在矩阵的每一行上。这种操作常用于多类别分类任务，其中每一行代表一个样本的原始分数或logits，而每个列代表一个类别。
    """

    def call(self, inputs):
        return tf.nn.softmax(tf.reshape(inputs, (-1, inputs.shape[-1])))

# 定义LogSoftmax类，继承自_L.Layer
class LogSoftmax(_L.Layer):
    """
    LogSoftmax（对数软最大值）是一种常用的激活函数，通常用于多类别分类问题中神经网络的输出层。它将输入的原始分数（logits）转化为对数概率分布，以便更好地处理数值稳定性和训练的问题。
    """
    def call(self, inputs):
        return tf.math.log_softmax(inputs)

__act_cls = locals()


def doc(show_doc=True):
    # 罗列所有以_L.Layer作为父类的类对象
    _doc = ""
    for _cls in __act_cls:
        # 判断_cls是不是class
        if isinstance(__act_cls[_cls], type) and issubclass(__act_cls[_cls], _L.Layer):
            _doc += __act_cls[_cls].__name__ + ((":" + __act_cls[_cls].__doc__) if show_doc else "") + "\n\n"
    return _doc


if __name__ == "__main__":
    print(doc())
