import os
import warnings
from dataset.type1 import _read1


class Messages:
    def __init__(self, filename, filetype=None):
        self.filename = filename
        if filetype != None:
            self.filetype = filetype
        else:
            self.filetype = 1
        self._setn = 0
        self.data = []
        self.__refresh = False
        self.refresh()

    def refresh(self):
        """
         从报文中提取出报文的全部信息：包含多少条报文，报文类型等
        """
        self.__refresh = False
        try:
            f = open(self.filename, "r")
            self.data = f.readlines()
            self._setn = len(self.data)
            self.refresh = True
        except:
            raise Exception("Cann't access the file {}".format(self.filename))
        f.close()
        return self.__refresh

    def getsets(self):
        """
        返回报文文件的报文条数
        """
        return self._setn

    def get_types(self):
        return self.filetype

    def ReadM(self, setn=None):
        dsct = []
        if setn is None:
            read_range = range(0, self._setn)
        else:
            read_range = range(0, setn)
        if self.refresh is False:
            if self.refresh() is False:
                raise Exception("cann't read from the file" + self.filename)
        for i in read_range:
            singled = self.data[i]
            dsct.append(self._read(singled))
        if len(dsct) == 1:
            dsct = dsct[0]
        return dsct

    def _read(self, singled):
        di = dict()
        if self.filetype == 1:
            di = _read1(singled)
            return di
