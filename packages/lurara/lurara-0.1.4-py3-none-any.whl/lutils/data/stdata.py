import os
import re

from files3 import files


# Standard Data Format
class StData:
    """
    定义了一种标准的数据集*.svoc, 构建了文件系统与标准数据集之间的桥梁. 只能在python代码中进行储存和读取
    xs, ys 或者 xs1, ys1  xs2, ys2 ... xsi, ysi ... xsn, ysn
    其中 xs, ys 均为list, x和y的类型没有明确限制,但x:object一般为ndarray, y:object一般为int|str
    上述两种格式均为支持的格式

    # -----------------------------------------------------------------

    一个数据集库只包含一种数据集格式, 即一个文件夹下只能包含一种数据集格式,最好不要将多个网络的数据集放在一个数据集库中管理
    每个数据集库按照index来管理, 比如len(stdata), stdata[i], 每个value为一个xs, ys

    """

    def __init__(self, fdir: str = ''):
        """

        :param fdir: 目标数据集所在的文件系统目录路径. 所有数据都将维护在此
        """
        assert isinstance(fdir, str), f"fdir must be str, not {type(fdir)}"
        fdir = re.sub('\s+$', '', fdir)
        fdir = re.sub('[\\/]+$', '', fdir)
        self.voc_f = files(fdir, '.svoc')
        self.voc_dir_name = os.path.dirname(fdir)

    def load(self, index):
        voc_list = self.voc_f.list()
        return self.voc_f[voc_list[index]]

    def save(self, xs, ys, mode: str = 'a', block_size: int = None):
        """
        保存数据到数据集库中
        :param xs:
        :param ys:
        :param mode: 'a' 'w' 两种, 'a'表示追加, 'w'表示覆盖(即会先清除所有原有数据集)
        :param block_size: None 用于将数据保存为多个部分, 每个部分的最大数据量. None表示保存到一个文件中
        :return:
        """
        mode = mode.lower()
        assert mode in ('a', 'w'), f"mode only accept 'a' or 'w', not {mode}"
        assert len(xs) == len(ys), f'xs and ys must have the same length, not {len(xs)} and {len(ys)}'
        if mode == 'w':
            del self.voc_f[:]

        # 计算要分成多少个block
        if block_size is None:
            block_num = 1
            block_size = len(xs)
        else:
            block_num = len(xs) // block_size
            if block_num * block_size < len(xs):
                block_num += 1

        ids = [-1] + [int(i) for i in self.voc_f.list()]
        id_max = max(ids) + 1

        for i in range(block_num):
            block_xs = xs[i * block_size: (i + 1) * block_size]
            block_ys = ys[i * block_size: (i + 1) * block_size]
            self.voc_f[str(i + id_max)] = block_xs, block_ys

    def __len__(self):
        return len(self.voc_f.list())

    def __getitem__(self, index):
        voc_list = self.voc_f.list()
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            xs, ys = [], []
            for i in range(start, stop, step):
                x, y = self.voc_f[voc_list[i]]
                xs.extend(x)
                ys.extend(y)
            return xs, ys
        else:
            return self.load(index)

    # readonly, no setitem