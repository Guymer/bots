# -*- coding: utf-8 -*-

def create_maps(dirOut, territories):
    # Import modules ...
    import os

    # Load sub-functions ...
    from .create_map import create_map

    # Loop over territories ...
    for territory in territories.iterkeys():
        # Make file path and create map (if needed) ...
        fpath = os.path.join(dirOut, territory.replace(" ", "_") + ".png")
        if not os.path.exists(fpath):
            create_map(territory, territories[territory], fpath)
