#coding: utf-8
import os
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from . import MODULE_DIR

logo_path = os.path.join(MODULE_DIR, "data/logo.png")
logo_img  = np.asarray(Image.open(logo_path))

def plot_logo(ax=None):
    if ax is None:
        fig, ax = plt.subplots()
    ax.imshow(logo_img)
    ax = ax_clear(ax)
    return ax

def ax_clear(ax, spines=True, label=True, scale=True):
    if spines:
        for k,v in ax.spines.items():
            v.set_visible(False)
    if label:
        ax.tick_params(labelbottom=False, labelleft=False, labelright=False, labeltop=False)
    if scale:
        ax.tick_params(bottom=False, left=False, right=False, top=False)
    return ax
