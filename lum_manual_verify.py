import matplotlib.pyplot as plot
from collections.abc import Callable

from lum import *

# This tool is NOT done being tested. Manual checking and good knowledge of 
# the relevant WCAG criteria is still strictly required.
# 
# Please mark where this tool is used as "flash.py". Future unit testing may 
# invalidate some or all of its results.
#     -- Leif

def verify_feature_routine(C1:ColorVector, C2:ColorVector, point_count:int):
    print(f"C1 = {C1}")
    print(f"C2 = {C2}")
    print()
    print(f"C1 for lum internal = {C1.as_internal_for_relative_luminance()}")
    print(f"C2 for lum internal = {C2.as_internal_for_relative_luminance()}")
    print()
    plot_colors_between(C1, C2, point_count)

    

def plot_colors_between(C1:ColorVector, C2:ColorVector, points:int, ylabel:str = "relative luminance", yfunction:Callable[[ColorVector], float] = ColorVector.get_relative_luminance):
    if (points < 2):
        raise ValueError(f"plot_colors_between ... parameter `points` cannot be less than 2 (was {points}).")

    steps = points - 1 

    # plot a graph of all values between the two selected...
    colinear_vectors:list[ColorVector] = list()
    delta_color = C2 - C1
    for i in range(steps):
        k:float = i / float(steps)
        new_vector:ColorVector = C1 + (delta_color * k)
        colinear_vectors.append(new_vector)
        print(f"[{i}] ... {new_vector}")
    colinear_vectors.append(C2)
    print(f"[last] ... {C2}")

    plot.plot([yfunction(vec) for vec in colinear_vectors])
    plot.ylabel(ylabel)
    plot.ylim((0.0, 1.0))
    plot.xlabel(f"lerp proportion (C1=0, C2={steps})")

    plot.show()

