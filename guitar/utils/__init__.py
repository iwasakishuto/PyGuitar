# coding: utf-8
import os
UTILS_DIR = os.path.dirname(os.path.abspath(__file__))
MODULE_DIR = os.path.dirname(UTILS_DIR) 
REPO_DIR = os.path.dirname(MODULE_DIR) 

from . import coloring_utils
from . import decorate_utils
from . import driver_utils
from . import guitar_utils
from . import mpatches_utils

from .coloring_utils import get_notes2color
from .coloring_utils import plot_notes_color_theme
from .coloring_utils import plot_notes_all_color_theme

from .decorate_utils import plot_logo
from .decorate_utils import ax_clear

from .driver_utils import driver_wrapper

from .guitar_utils import split_chord
from .guitar_utils import get_notes
from .guitar_utils import get_intervals
from .guitar_utils import find_notes_positions
from .guitar_utils import find_key_major_scale

from .mpatches_utils import mpatches