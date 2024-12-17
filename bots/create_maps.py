#!/usr/bin/env python3

# Define function ...
def create_maps(
    dirOut,
    territories,
    /,
    *,
        debug = __debug__,
        nIter = 100,
    onlyValid = False,
       repair = False,
      timeout = 60.0,
):
    """Create maps of all the territories

    This function creates PNG maps of all of the countries in all of the
    territories.

    Parameters
    ----------
    dirOut : str
        the path to save the PNGs in
    territories : dict
        the database
    debug : bool, optional
        print debug messages
    nIter : int, optional
        the maximum number of iterations (particularly the Vincenty formula)
    onlyValid : bool, optional
        only return valid Polygons (checks for validity can take a while, if
        being called often)
    repair : bool, optional
        attempt to repair invalid Polygons
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
            create_map(
                territory,
                territories[territory],
                fpath,
                    debug = debug,
                    nIter = nIter,
                onlyValid = onlyValid,
                   repair = repair,
                  timeout = timeout,
            )
