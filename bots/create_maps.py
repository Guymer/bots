#!/usr/bin/env python3

# Define function ...
def create_maps(dirOut, territories, /):
    """Create maps of all the territories

    This function creates PNG maps of all of the countries in all of the
    territories.

    Parameters
    ----------
    dirOut : str
        the path to save the PNGs in
    territories : dict
        the database
    """

    # Import standard modules ...
    import os

    # Import sub-functions ...
    from .create_map import create_map

    # Loop over territories ...
    for territory in territories.keys():
        # Make file path and create map (if needed) ...
        fpath = f"{dirOut}/{territory}.png"
        if not os.path.exists(fpath):
            create_map(territory, territories[territory], fpath)
