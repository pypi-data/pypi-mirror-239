# -*- coding: UTF-8 -*-
# pip install opencv-python
import pyuc
from pyuc.py_api_b import PyApiB
from PIL import Image,ImageFilter
from pyuc.py_recg.imgU import ImgU
if PyApiB.tryImportModule("aircv", installName="aircv"):
    import aircv as ac
if PyApiB.tryImportModule("cv2", installName="opencv-python"):
    import cv2
if PyApiB.tryImportModule("pytesseract", installName="pytesseract"):
    import pytesseract 
    # https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe
    # tesseract --list-langs 
    # 训练下载：https://github.com/nguyenq/jTessBoxEditor/releases/tag/


class TesseractU(PyApiB):
    """
    文字识别相关工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def image_to_num(self,imgU:ImgU, lang="eng", config="--psm 7 -c tessedit_char_whitelist=0123456789."):
        return pytesseract.image_to_string(imgU.getPilImg(),lang=lang,config=config)

    def train(self):
        pass

    
