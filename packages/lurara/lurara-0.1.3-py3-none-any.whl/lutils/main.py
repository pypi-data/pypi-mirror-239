import os

import numpy as np
import tensorflow as tf
from files3 import files
from typing import Tuple
from keras import layers as _L
from keras import Model, Input
from keras.callbacks import EarlyStopping
from keras.models import load_model
from Lutils._basic import *
from Lutils.data import DataControl


class LModel:
    """
    一个用于构建和管理机器学习模型的类。

    属性:
        patience: 一个整数，表示早停法的耐心值。
        data: 一个DataControl对象，用于控制数据的加载和处理。
        model: 一个tf.keras.Model对象，用于表示机器学习模型。
        optimizer: 一个tf.keras.optimizers对象，用于指定模型的优化器。
        loss: 一个tf.keras.losses对象或函数，用于指定模型的损失函数。
        metrics: 一个列表，包含tf.keras.metrics对象或函数，用于指定模型的评估指标。
        weighted_metrics: 一个列表，包含tf.keras.metrics对象或函数，用于指定模型的加权评估指标。
        callbacks: 一个列表，包含tf.keras.callbacks对象，用于指定模型的回调函数。
        batch_size: 一个整数，表示模型训练和评估时的批次大小。
        validation_split: 一个浮点数，表示从训练数据中划分出验证数据的比例。
    """

    patience = 10

    @property
    def trainable(self):
        """
        返回模型的训练状态。
        :return:
        """
        return self.model.trainable

    @trainable.setter
    def trainable(self, value):
        """
        对模型中的所有层设置是否可训练。
        :param value:
        :return:
        """
        for layer in self.model.layers:
            layer.trainable = value

    def __init__(self, input: Input, output:tf.Tensor, data_ctrl:DataControl=None, name=None):
        """
        初始化LModel类的实例。

        参数:
            input: 一个tf.keras.Input对象或列表，表示模型的输入层。
            output: 一个tf.Tensor对象或列表，表示模型的输出层。
            data_ctrl: 一个DataControl类或其子类，用于控制数据的加载和处理。
        异常:
            Exception: 如果data_ctrl不是DataControl类或其子类，或者无法创建DataControl实例，则抛出异常。
        """
        self.data:DataControl = data_ctrl
        if self.data is None:
            ...
        elif not isinstance(data_ctrl, DataControl):
            try:
                self.data = data_ctrl()
            except Exception as err:
                raise Exception(f"\n\nFailed to create DataControl instance. data_ctrl:{type(data_ctrl)}\n\terror info:\n\t{err}")

        # if input is None or output is None:
        #     raise ValueError(f"\n\ninput and output must be specified.\n\tinput:{input}\n\toutput:{output}")
        # else:
        #     self.model: Model = Model(inputs=input, outputs=output)
        self.model: Model = Model(inputs=input, outputs=output, name=name)

        # --------------------------------------------------------------------------------------------------------------
        self.optimizer = None
        self.loss = None
        self.metrics = None

        self.weighted_metrics = None
        self.callbacks = [EarlyStopping(patience=LModel.patience)]
        self.batch_size = None
        self.validation_split = 0.1

    def _check_model(self):
        assert self.model is not None, "Model is not defined. Please use .load(path) to load a model"
        assert isinstance(self.model, Model), f"Model is not a keras Model. Got {type(self.model)}"

    def _check_data(self):
        assert self.data is not None, "DataControl is not defined. Please use .set_data(DataControl) to set a data"
        assert isinstance(self.data, DataControl), f"DataControl is not a DataControl. Got {type(self.data)}"

    def config(self,
               optimizer=None,
               loss=None,
               metrics=None,
               weighted_metrics=None,
               callbacks=None,
               batch_size=None,
               validation_split=None):
        if optimizer is not None:
            self.optimizer = optimizer
        if loss is not None:
            self.loss = loss
        if metrics is not None:
            self.metrics = metrics
        if weighted_metrics is not None:
            self.weighted_metrics = weighted_metrics
        if callbacks is not None:
            _flag = False
            for each in callbacks:
                if isinstance(each, EarlyStopping):
                    _flag = True
                    break
            if not _flag:
                callbacks.append(EarlyStopping(patience=LModel.patience, restore_best_weights=True))
            self.callbacks = callbacks
        if batch_size is not None:
            self.batch_size = batch_size
        if validation_split is not None:
            if validation_split < 0.01:
                raise ValueError("validation_split should be >= 0.01")
            self.validation_split = validation_split

    def train(self, times:int=1, num=None, percent:float=1.0):
        """
        训练模型
        :param times: 训练的次数（轮数），默认为1
        :param num: 训练的数据量，如果指定了，就按照这个数量从数据集中随机抽取数据，否则按照percent参数来确定数据量
        :param percent: 训练的数据占总数据集的百分比，只有在num参数为空时才有效，默认为1.0（即使用全部数据）
        :return: 一个训练历史对象，包含了训练过程中的损失和评估指标等信息
        """
        self._check_model()
        self._check_data()
        self.model.compile(optimizer=self.optimizer, loss=self.loss, metrics=self.metrics, weighted_metrics=self.weighted_metrics)

        _x, _y = self.data(num, percent)  # num优先级高于percent

        # print(f"len of x: {len(_x)}, len of y: {len(_y)}")
        _x = np.array(_x)
        _y = np.array(_y)

        his = self.model.fit(_x, _y, shuffle=True, batch_size=self.batch_size, epochs=times, validation_split=self.validation_split, callbacks=self.callbacks)
        return his

    def predict(self, input, pre=True, raw=False, label=False) -> object:
        """
       预测一个输入的输出结果
       :param input: 一个输入，可以是任意类型
       :param pre: 是否启用预处理，默认为True
       :param raw: 是否返回原始的输出结果，默认为False
       :param label: 是否返回输出结果的标签，默认为False
       :return: 一个输出结果，根据raw和label的设置，可能是一个数字、一个字符串或一个对象
       """
        self._check_model()
        self._check_data()
        if pre:
            input = self.data.prehandle(input)
        _result = self.model.predict(np.array(input).reshape((1, -1)))[0]
        if raw:
            return _result
        _result = self.data.output2label(_result)
        if label:
            return _result
        return self.data.posthandle(_result)

    def predicts(self, inputs: list, pre=True, raw=False, label=False) -> list:
        """
        预测一组输入的输出结果
        :param inputs: 一个输入的列表，每个输入可以是任意类型
        :param pre: 是否启用预处理，默认为True
        :param raw: 是否返回原始的输出结果，默认为False
        :param label: 是否返回输出结果的标签，默认为False
        :return: 一个输出结果的列表，根据raw和label的设置，每个输出结果可能是一个数字、一个字符串或一个对象
        """
        self._check_model()
        self._check_data()
        if pre:
            inputs = [self.data.prehandle(input) for input in inputs]
        _results = self.model.predict(np.array(inputs))
        if raw:
            return _results
        _results = [self.data.output2label(_result for _result in _results)]
        if label:
            return _results
        return [self.data.posthandle(_result) for _result in _results]

    def save(self, name):
        """
        保存模型权重到指定路径。

        参数:
            name: 表示保存模型的名称。

        异常:
            Exception: 如果没有创建模型，则抛出异常。
        """
        self._check_model()
        self.model.save_weights(name)


    def load(self, name):
        """
        从指定路径加载模型权重。
        * 注意: 若已创建模型，则会覆盖。

        参数:
            name: 表示保存模型的名称。

        异常:
            Exception: 如果没有创建模型，则抛出异常。
        """
        self.model.load_weights(name)
        self._check_model()

    def summary(self):
        """
        打印模型的摘要信息。
        """
        self._check_model()
        self.model.summary()

    def set_data(self, data):
        self.data = data
        self._check_data()

    def __str__(self):
        return self.model.name + "(LModel){" + f"inputs={self.model.input_shape}, outputs={self.model.output_shape}"  + "}"

    def __call__(self, inputs, *args, **kwargs):
        self._check_model()
        return self.model(inputs, *args, **kwargs)
