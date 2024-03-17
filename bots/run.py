#!/usr/bin/env python3

# Define function ...
def run(dirOut, /, *, n = 10):
    """Run BOTS

    This is a wrapper function to call all of the functions in BOTS to create
    the JSON database, the PNG maps and the PNG timeline.

    Parameters
    ----------
    dirOut : str
        the path to save the database and PNGs in
    n : int, optional
        the number of days to survey
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
        create_db(dbpath)

    # Load database ...
    with open(dbpath, "rt", encoding = "utf-8") as fObj:
        territories = json.load(fObj)

    # Create BOT maps ...
    create_maps(dirOut, territories)

    # Create timeline ...
    create_timeline(dirOut, territories, n = n)
