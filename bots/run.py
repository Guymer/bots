#!/usr/bin/env python3

# Define function ...
def run(
    dirOut,
    /,
    *,
        debug = __debug__,
            n = 10,
        nIter = 100,
    onlyValid = False,
       repair = False,
      timeout = 60.0,
):
    """Run BOTS

    This is a wrapper function to call all of the functions in BOTS to create
    the JSON database, the PNG maps and the PNG timeline.

    Parameters
    ----------
    dirOut : str
        the path to save the database and PNGs in
    debug : bool, optional
        print debug messages
    n : int, optional
        the number of days to survey
    nIter : int, optional
        the maximum number of iterations (particularly the Vincenty formula)
    onlyValid : bool, optional
        only return valid Polygons (checks for validity can take a while, if
        being called often)
    repair : bool, optional
        attempt to repair invalid Polygons
    timeout : float, optional
        the timeout for any requests/subprocess calls
    """

    # Import standard modules ...
    import json
    import os

    # Import sub-functions ...
    from .create_db import create_db
    from .create_maps import create_maps
    from .create_timeline import create_timeline

    # Make output directory ...
    if not os.path.exists(dirOut):
        os.makedirs(dirOut)

    # Make database path and create database (if needed) ...
    dbpath = f"{dirOut}/db.json"
    if not os.path.exists(dbpath):
        create_db(
            dbpath,
            onlyValid = onlyValid,
               repair = repair,
        )

    # Load database ...
    with open(dbpath, "rt", encoding = "utf-8") as fObj:
        territories = json.load(fObj)

    # Create BOT maps ...
    create_maps(
        dirOut,
        territories,
            debug = debug,
            nIter = nIter,
        onlyValid = onlyValid,
           repair = repair,
    )

    # Create timeline ...
    create_timeline(
        dirOut,
        territories,
          debug = debug,
              n = n,
        timeout = timeout,
    )
