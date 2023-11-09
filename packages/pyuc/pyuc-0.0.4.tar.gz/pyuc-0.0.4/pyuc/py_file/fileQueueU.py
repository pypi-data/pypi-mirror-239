# -*- coding: UTF-8 -*-
from pyuc.py_api_b import PyApiB
import time
import os


class FileQueueU(PyApiB):
    """
    文件做中间件的队列工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    @property
    def filePath(self):
        __filePath = getattr(self, "__filePath", None)
        if __filePath == None:
            __filePath = self._signKey
            setattr(self, "__filePath", __filePath)
        return __filePath

    @filePath.setter
    def filePath(self, path:str):
        setattr(self, "__filePath", path)

    def push(self, msg):
        with open(self.filePath, "a") as pipe:
            pipe.write(f"{msg}\n")

    def __prapareFile__(self):
        if not os.path.exists(self.filePath):
            with open(self.filePath, "a") as pipe:
                pipe.write(f"")

    def toList(self) -> list:
        """ 不增不减返回所有内容 """
        self.__prapareFile__()
        lines = []
        with open(self.filePath, "r+") as pipe:
            lines = pipe.readlines()
        return lines

    def pop(self, isWait=True):
        """ 从队尾先出（先进先出） """
        data = None
        self.__prapareFile__()
        with open(self.filePath, "r+") as pipe:
            lines = pipe.readlines()
            while isWait and (not lines):
                time.sleep(0.01)
                lines = pipe.readlines()
            if lines:
                data = lines[-1].rstrip()
                pipe.seek(0)
                pipe.writelines(lines[:-1])
                pipe.truncate()
        return data

    def popl(self, isWait=True):
        """ 从队尾先出（先进先出） """
        return self.pop(isWait)

    def poll(self, isWait=True):
        """ 从队头出（先进先晚） """
        data = None
        self.__prapareFile__()
        with open(self.filePath, "r+") as pipe:
            lines = pipe.readlines()
            while isWait and (not lines):
                time.sleep(0.01)
                lines = pipe.readlines()
            if lines:
                data = lines[0].rstrip()
                pipe.seek(0)
                pipe.writelines(lines[1:])
                pipe.truncate()
        return data
