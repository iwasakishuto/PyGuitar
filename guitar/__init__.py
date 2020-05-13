# coding: utf-8
import os

LIB_DIR_PATH  = os.path.dirname(os.path.abspath(__file__))
REPO_DIR_PATH = os.path.dirname(LIB_DIR_PATH)
DATA_DIR_PATH = os.path.join(REPO_DIR_PATH, "data")

from . import main

from .main import Guitar
