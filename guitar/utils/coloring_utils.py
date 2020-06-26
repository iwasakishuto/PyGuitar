# coding: utf-8
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.cm as cm
from guitar.env import *
from kerasy.utils import chooseTextColor, handleTypeError

def plot_notes_color_theme(theme, radius=0.3, fontsize=20):
    """
    @params theme : (str) Color theme for `matplotlib.cm.cmap_d`
    """
    if isinstance(theme, matplotlib.colors.ListedColormap) or \
        isinstance(theme, matplotlib.colors.LinearSegmentedColormap):
        cmap = theme
        theme = cmap.name
    elif isinstance(theme, str):
        cmap = cm.cmap_d.get(theme)
    else:
        handleTypeError(types=[str, matplotlib.colors.ListedColormap, matplotlib.colors.LinearSegmentedColormap], theme=theme)

    fig, ax = plt.subplots(figsize=(12,1))
    ax.set_xlim(-0.5,11.5); ax.set_ylim(-0.5,0.5)
    ax.set_title(theme)
    for i,note in enumerate(NOTES):   
        rgba = cmap(i/LEN_OCTAVES)
        fc = chooseTextColor(rgba[:3], ctype="rgb", max_val=1)
        ax.add_patch(mpatches.Circle(xy=(i, 0), radius=radius, color=rgba))
        ax.annotate(s=note, xy=(i, 0), color=fc, weight='bold', fontsize=fontsize, ha='center', va='center')
    plt.show()
    
def plot_notes_all_color_theme(radius=0.3, fontsize=20):
    for name, cmap in cm.cmap_d.items():
        plot_notes_color_theme(cmap, radius=radius, fontsize=fontsize)