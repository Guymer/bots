# -*- coding: utf-8 -*-

def run(dirOut = "BOTSoutput"):
    # Import modules ...
    import json
    import os

    # Load sub-functions ...
    from .create_db import create_db
    from .create_maps import create_maps
    from .create_timeline import create_timeline

    # Make database path and create database (if needed) ...
    dbpath = os.path.join(dirOut, "db.json")
    if not os.path.exists(dbpath):
        create_db(dbpath)

    # Load database ...
    territories = json.load(open(dbpath, "rt"))

    # Create BOT maps ...
    create_maps(dirOut, territories)

    # Create timeline ...
    create_timeline(dirOut, territories)
