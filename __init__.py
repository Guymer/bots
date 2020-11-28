"""
British Overseas Territories Sunsets (BOTS)

This Python 3.x module contains all the functions required to calculate the
sunrises and sunsets of all territories in the BOT. It uses this data to
demonstrate that the sun has not (yet) set over the BOT.
"""

# Import standard modules ...
import sys

# Import sub-functions ...
from .create_db import create_db
from .create_map import create_map
from .create_maps import create_maps
from .create_timeline import create_timeline
from .run import run

# Ensure that this module is only imported by Python 3.x ...
if sys.version_info.major != 3:
    raise Exception("the Python module \"bots\" must only be used with Python 3.x") from None