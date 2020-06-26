#coding: utf-8
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def x_mark(xy, radius=5, **kwargs):
    x,y = xy
    r = radius
    return plt.Polygon(xy=(
        (x, y-0.5*r), (x+0.5*r, y-r), (x+r, y-0.5*r),
        (x+0.5*r, y), (x+r, y+0.5*r), (x+0.5*r, y+r),
        (x, y+0.5*r), (x-0.5*r, y+r), (x-r, y+0.5*r),
        (x-0.5*r, y), (x-r, y-0.5*r), (x-0.5*r, y-r), 
    ), closed=True, **kwargs)

def star_hexagon(xy, radius=5, **kwargs):
    """
        |\
     c  | \  b
        |__\  
         a
    """
    x,y = xy
    r = radius
    a = 1/4*r
    b = a*2
    c = a*3**(1/2)
    return plt.Polygon(xy=(
        (x, y-2*c), (x+a, y-c), (x+a+b, y-c),
        (x+b, y), (x+a+b, y+c), (x+a, y+c),
        (x, y+2*c), (x-a, y+c), (x-a-b, y+c),
        (x-b, y), (x-a-b, y-c), (x-a, y-c),
    ), closed=True, **kwargs)

mpatches.x_mark = x_mark
mpatches.star_hexagon = star_hexagon