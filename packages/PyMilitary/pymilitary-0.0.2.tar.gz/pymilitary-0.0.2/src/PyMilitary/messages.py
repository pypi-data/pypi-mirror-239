import os
import warnings
import numpy as np
from dataset.type1 import _read1
class Messages:
    def __init__(self,filename,filetype=None):
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
            f = open(self.filename,"r")
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
    def ReadM(self, fsetn=None, tsetn=None):
        dsct = []
        if fsetn is None and tsetn is None:
            read_range = range(0,self._setn)
        elif fsetn is None and tsetn:
            read_range = range(0,tsetn)
        elif fsetn and tsetn is None:
            read_range = range(fsetn, self._setn)
        elif fsetn and tsetn:
            read_range = range(fsetn, tsetn)
        if self.refresh is False:
            if self.refresh() is False:
                raise Exception("cann't read from the file"+self.filename)
        for i in read_range:
            singled = self.data[i]
            try:
                dsct.append(self._read(singled))
            except IndexError as eer:
                print("读取的报文条数过多，请合理设置需要读取的报文长度")
        if len(dsct) == 1:
            dsct = dsct[0]
        return dsct

    def _read(self, singled):
        di = dict()
        if self.filetype ==1:
            di = _read1(singled)
            return di