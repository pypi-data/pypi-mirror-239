from typing import Tuple, Iterable
from copy import deepcopy
from abc import ABCMeta, abstractmethod
import numpy as np


class WeakReadonlyList(list):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)

    def __setitem__(self, key, value):
        raise RuntimeError("readonly list")

    def __delitem__(self, key):
        raise RuntimeError("readonly list")

    def append(self, value):
        raise RuntimeError("readonly list")

    def extend(self, values):
        raise RuntimeError("readonly list")

    def insert(self, index, value):
        raise RuntimeError("readonly list")

    def pop(self, index):
        raise RuntimeError("readonly list")

    def remove(self, value):
        raise RuntimeError("readonly list")

    def clear(self) -> None:
        raise RuntimeError("readonly list")

    def system_append(self, value):
        super().append(value)

    def system_extend(self, values):
        super().extend(values)

    def system_insert(self, index, value):
        super().insert(index, value)

    def system_pop(self, index):
        return super().pop(index)

    def system_remove(self, value):
        super().remove(value)

    def system_setitem(self, key, value):
        super().__setitem__(key, value)

    def system_delitem(self, key):
        super().__delitem__(key)

    def system_clear(self):
        super().clear()

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return super().__repr__()

    def __iadd__(self, other):
        raise RuntimeError("readonly list")


__cls_types = []


class DataIO(metaclass=ABCMeta):
    @abstractmethod
    def label2output(self, label: object) -> np.ndarray:
        """
        trans label to output
        :param label: object, general in float or str
        :return: output: ndarray, shape = model.output_shape[1:]
        """
        pass

    @abstractmethod
    def output2label(self, output: np.ndarray) -> object:
        """
        trans output to label
        :param output: ndarray, shape = model.output_shape[1:]
        :return: labels: object, general in float or str
        """
        pass


class DataPool(DataIO, metaclass=ABCMeta):
    def __new__(cls, *args, **kwargs):
        inst = super().__new__(cls)
        inst._bufx = []
        inst._bufy = []
        return inst

    @property
    def pool(self) -> Tuple[WeakReadonlyList, WeakReadonlyList]:
        return self._pool

    @property
    def x(self) -> WeakReadonlyList:
        return self._pool[0]

    @property
    def xshape(self) -> tuple:
        if len(self._pool[0]) == 0:
            raise ValueError("No any data in pool. Can not get the shape.")
        return np.array(self._pool[0][0]).shape

    @property
    def y(self) -> WeakReadonlyList:
        return self._pool[1]

    @property
    def yshape(self) -> tuple:
        if len(self._pool[1]) == 0:
            raise ValueError("No any data in pool. Can not get the shape.")
        return np.array(self._pool[1][0]).shape

    def __init__(self):
        self._pool: Tuple[WeakReadonlyList, WeakReadonlyList] = WeakReadonlyList(), WeakReadonlyList()  # x_list, y_list
        self._left = self.load(None)
        self._flag = False  # 是否已使用 FLAG | 一般只有第一次有效

    def __getitem__(self, item):
        if isinstance(item, str):
            if item.lower() == 'x':
                return self._pool[0]
            elif item.lower() == 'y':
                return self._pool[1]
            else:
                raise ValueError(f"'{item}' is not a valid str item")
        else:
            return self._pool[0][item], self._pool[1][item]

    def __len__(self):
        return len(self._pool[0])

    def append(self, x: np.ndarray, y: object):
        self._pool[0].system_append(x)
        self._pool[1].system_append(y)

    def extend(self, x: list, y: list):
        assert len(x) == len(y), f"x and y must have the same length, but x={len(x)}, y={len(y)}"
        self._pool[0].system_extend(x)
        self._pool[1].system_extend(y)

    def clear(self):
        self._pool[0].system_clear()
        self._pool[1].system_clear()

    @abstractmethod
    def load(self, left=None) -> None:
        pass

    @abstractmethod
    def augments(self, xs, ys) -> tuple:
        """
        对xs ys进行数据增强
        发生在call的第2. 进行数据增强
        :param xs:
        :param ys:
        :return:
        """
        pass

    @abstractmethod
    def prehandle(self, x) -> np.ndarray:
        pass

    @abstractmethod
    def posthandle(self, y) -> object:
        pass

    def __call__(self, num:int=None, percent:float=None):
        if num is None:
            if percent is None:
                raise ValueError('num or percent must be specified')

            assert (0 - 1e-6) <= percent <= (1 + 1e-6), 'percent must be in [0, 1]'
            num = int(len(self) * percent)
            if num <= 0:
                raise ValueError(f'Not enough data to train. at persent={percent}')


        while num > len(self._bufx):
            if self._flag and self._left is not None:
                self._left = self.load(self._left)
            self._bufx.extend(self._pool[0].copy())
            self._bufy.extend(self._pool[1].copy())
            self._flag = True

        _x, self._bufx = self._bufx[:num], self._bufx[num:]
        _y, self._bufy = self._bufy[:num], self._bufy[num:]

        _x, _y = self.augments(_x, _y)

        for i in range(len(_x)):
            _x[i] = self.prehandle(_x[i])
        for i in range(len(_y)):
            _y[i] = self.label2output(_y[i])
        return _x, _y


class DataControl(DataPool, metaclass=ABCMeta):
    @abstractmethod
    def label2output(self, label: object) -> np.ndarray:
        """
        trans label to output
        :param label: object, general in float or str
        :return: output: ndarray, shape = model.output_shape[1:]
        """
        pass

    @abstractmethod
    def output2label(self, output: np.ndarray) -> object:
        """
        trans output to label
        :param output: ndarray, shape = model.output_shape[1:]
        :return: labels: object, general in float or str
        """
        pass

    @abstractmethod
    def load(self, left=None) -> None:
        """
        load data from somewhere into self

        self.append(x: np.ndarray, y: object)
        self.x or self['x'] to get the WeakReadonlyList
        self.y or self['y'] to get the WeakReadonlyList
        self[?] to get the x[?], y[?]

        :param left: 上次调用load时, load的返回值, 应该是float. 第一次调用时传入None
        :return: left, 剩余量, 是一个float, 0 - 1, 如果一次就读完了, 返回None
        """
        pass

    # --------------------------------------------------------------------------
    # 下面是可选的方法:
    def augments(self, xs, ys) -> tuple:
        """
        对xs ys进行数据增强
        发生在call的第2. 进行数据增强
        :param xs:
        :param ys:
        :return:
        """
        return xs, ys


    def prehandle(self, x) -> np.ndarray:
        """
        对x进行预处理
        原理:
        预处理只在__call__以及LModel.predict中被调用, 其余方式获取x y都是原始的数据

        __call__的调用顺序:
        1. 取出原始数据集中的一部分.
        2. 进行数据增强
        3. 对每个数据的x进行预处理             <----------------------------------
        4. 将每个数据的y(label)转换为y(stdandard output)
        -> 最后返回 List[type(x)], List[type(y_output)]

        :param x: np.ndarray, shape = (?, ?)
        :return: x
        """
        return x

    def posthandle(self, y) -> object:
        """
        对y进行后处理
        原理:
        后处理只在LModel.predict函数中被调用
        当模型输出结果后:   :raw=False, label=False
        1. 先将y_pred(output)转化为y_pred(label)
        2. 然后对y_pred(label)进行后处理             <----------------------------------
        -> 最后返回'后处理'返回的结果

        *如果希望predict返回output, 那么调用函数时指定raw=True; (优先级更高)
        *如果希望predict返回label, 那么调用时指定参数label=True;
        :param y: object
        :return: y
        """
        return y

if __name__ == "__main__":
    class MyData(DataControl):
        def load(self):
            self.extend([1, 2, 3], [4, 5, 6])
            return True

        def labels2outputs(self, labels: Iterable) -> np.ndarray:
            return np.array(labels)

        def outputs2labels(self, outputs: np.ndarray) -> Iterable:
            return outputs


    class MyData2(MyData):
        ...

    pool = MyData()
    print(isinstance(MyData2, MyData))
