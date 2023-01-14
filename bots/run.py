#!/usr/bin/env python3

# Define function ...
def run(kwArgCheck = None, dirOut = "BOTSoutput", n = 10):
    # Import standard modules ...
    import json
    import os

    # Import sub-functions ...
    from .create_db import create_db
    from .create_maps import create_maps
    from .create_timeline import create_timeline

    # Check keyword arguments ...
    if kwArgCheck is not None:
        print(f"WARNING: \"{__name__}\" has been called with an extra positional argument")

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
