def run(dirOut = "BOTSoutput"):
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
    dbpath = os.path.join(dirOut, "db.json")
    if not os.path.exists(dbpath):
        create_db(dbpath)

    # Load database ...
    with open(dbpath, "rt", encoding = "utf-8") as fobj:
        territories = json.load(fobj)

    # Create BOT maps ...
    create_maps(dirOut, territories)

    # Create timeline ...
    create_timeline(dirOut, territories)
