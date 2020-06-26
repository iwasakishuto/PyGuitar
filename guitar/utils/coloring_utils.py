# coding: utf-8
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.cm as cm
from guitar.env import *
from kerasy.utils import chooseTextColor, handleTypeError

from ..env import LEN_OCTAVES

def get_notes2color(theme="rainbow"):
    notes2color={}
    for i,note in enumerate(NOTES):
        rgba = cm.cmap_d.get(theme)(i/LEN_OCTAVES)
        notes2color[note] = (rgba, chooseTextColor(rgb=rgba[:3], ctype="rgb", max_val=1))
    return notes2color

def plot_notes_color_theme(theme="rainbow", radius=0.3, fontsize=20, title=True, ax=None, fig=None):
    if isinstance(theme, matplotlib.colors.ListedColormap) or \
        isinstance(theme, matplotlib.colors.LinearSegmentedColormap):
        cmap = theme
        theme = cmap.name
    elif isinstance(theme, str):
        cmap = cm.cmap_d.get(theme)
    else:
        handleTypeError(types=[str, matplotlib.colors.ListedColormap, matplotlib.colors.LinearSegmentedColormap], theme=theme)

    if ax is None:
        fig, ax = plt.subplots(figsize=(LEN_OCTAVES,1))
    ax.set_xlim(-0.5, 11.5)
    if title: ax.set_title(theme)
    # Plot notes with color.
    for i,note in enumerate(NOTES):   
        rgba = cmap(i/LEN_OCTAVES)
        fc = chooseTextColor(rgba[:3], ctype="rgb", max_val=1)
        ax.add_patch(mpatches.Circle(xy=(i, 0), radius=radius, color=rgba))
        ax.annotate(s=note, xy=(i, 0), color=fc, weight='bold', fontsize=fontsize, ha='center', va='center')
    # Adjust for different sized figures.
    if fig is not None:
        bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        w,h = bbox.width, bbox.height
        height = 1/2 * h * (LEN_OCTAVES/w)
        ax.set_ylim(-height, height)
    return ax
    
def plot_notes_all_color_theme(radius=0.3, fontsize=20):
    for name, cmap in cm.cmap_d.items():
        plot_notes_color_theme(cmap, radius=radius, fontsize=fontsize)