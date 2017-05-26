import matplotlib
import matplotlib.cm as mplcm
import numpy as np
import cycler
from husl import husl_to_rgb

def colorcycler(i,cmap=mplcm.gist_rainbow):
    if not issubclass(cmap.__class__, matplotlib.colors.Colormap):
        try:
            cmap = mplcm.get_cmap(cmap)
        except ValueError as err:
            raise
    def cycler(j):
        return(cmap((j/(i+np.pi/10))%1))
    return(cycler)

def huslcycler(i,s=95,l=50,o=0):
    cycle = cycler.cycler(color=[husl_to_rgb(360*((o + j/i)%1),s,l) for j in range(i)])
    return(cycle)


def recolor_by_label(ax, fontsize=None):
    [tl.set_color(ax.xaxis.get_label().get_color()) for tl in
    ax.get_xticklabels()]
    [tl.set_color(ax.yaxis.get_label().get_color()) for tl in
    ax.get_yticklabels()]
    ax.xaxis.get_offset_text().set_color(ax.xaxis.get_label().get_color())
    ax.yaxis.get_offset_text().set_color(ax.yaxis.get_label().get_color())
    if fontsize is not None:
        [tl.set_fontsize(fontsize) for tl in ax.get_xticklabels()]
        [tl.set_fontsize(fontsize) for tl in ax.get_yticklabels()]

