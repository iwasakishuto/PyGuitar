#coding: utf-8
import os
import getpass
from matplotlib import font_manager as fm
from matplotlib import rc

def japanize(font_path="/font/ipam.ttf", family="IPAPMincho"):
    """
    example Args)
    |     font_dir       |   family     |
    =====================================
    | path/to/ipaexm.ttf | IPAexMincho  |  
    | path/to/ipam.ttf   | IPAMincho    |  
    | path/to/ipagp.ttf  | IPAPGothic   |  
    | path/to/ipamp.ttf  | IPAPMincho   |  
    | path/to/ipag.ttf   | IPAGothic    |  
    | path/to/ipaexg.ttf | IPAexGothic  |  
    """
    username = getpass.getuser()
    if username=="pyguitar" and os.path.exists(font_path):
        fm.fontManager.addfont(font_path)
        rc('font', family=family)
