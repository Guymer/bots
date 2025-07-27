#!/usr/bin/env python3

# Define function ...
def create_db(
    dbpath,
    /,
    *,
    onlyValid = False,
       repair = False,
):
    """Create the database of points

    This function creates a database of all of the points along the coastline(s)
    of each country in each territory.

    Parameters
    ----------
    dbpath : str
        the path to save the database
    onlyValid : bool, optional
        only return valid Polygons (checks for validity can take a while, if
        being called often)
    repair : bool, optional
        attempt to repair invalid Polygons
    """

    # Import standard modules ...
    import json
    import os
    import pathlib

    # Import special modules ...
    try:
        import cartopy
        cartopy.config.update(
            {
                "cache_dir" : pathlib.PosixPath("~/.local/share/cartopy_cache").expanduser(),
            }
        )
    except:
        raise Exception("\"cartopy\" is not installed; run \"pip install --user Cartopy\"") from None

    # Import my modules ...
    try:
        import pyguymer3
        import pyguymer3.geo
    except:
        raise Exception("\"pyguymer3\" is not installed; run \"pip install --user PyGuymer3\"") from None

    # Create dictionary of countries ...
    territories = {
        "United Kingdom" : {
            "countries" : ["United Kingdom"],
            "locations" : [(-0.000500, 51.476852)],
        },
        "Akrotiri & Dhekelia" : {
            "countries" : ["Akrotiri", "Dhekelia"],
        },
        "Anguilla" : {
            "countries" : ["Anguilla"],
        },
        "British Antarctic Territory" : {
            "countries" : ["Antarctica"],
            "locations" : [(-50.0, -90.0)],
        },
        "Bermuda" : {
            "countries" : ["Bermuda"],
        },
        "Cayman Islands" : {
            "countries" : ["Cayman Is."],
        },
        "Falkland Islands" : {
            "countries" : ["Falkland Is."],
        },
        "Gibraltar" : {
            "countries" : ["Gibraltar"],
        },
        "South Georgia & the South Sandwich Islands" : {
            "countries" : ["S. Geo. and the Is."],
        },
        "British Indian Ocean Territory" : {
            "countries" : ["Br. Indian Ocean Ter."],
        },
        "Montserrat" : {
            "countries" : ["Montserrat"],
        },
        "Pitcairn Islands" : {
            "countries" : ["Pitcairn Is."],
        },
        "Saint Helena, Ascension & Tristan da Cunha" : {
            "countries" : ["Saint Helena"],
            "locations" : [(-14.3559158, -7.9467166), (-12.2776838, -37.1052489)],
        },
        "Turks and Caicos Islands" : {
            "countries" : ["Turks and Caicos Is."],
        },
        "British Virgin Islands" : {
            "countries" : ["British Virgin Is."],
        },
    }

    # Find file containing all the country shapes ...
    sfile = cartopy.io.shapereader.natural_earth(
        resolution = "10m",
          category = "cultural",
              name = "admin_0_countries",
    )

    # Loop over territories ...
    for territory in sorted(list(territories.keys())):
        print(f"Finding locations for \"{territory}\" ...")

        # Create empty list ...
        territories[territory]["coords"] = []

        # Check if countries are defined ...
        if "countries" in territories[territory]:
            # Loop over records ...
            for record in cartopy.io.shapereader.Reader(sfile).records():
                # Create short-hand ...
                neName = pyguymer3.geo.getRecordAttribute(record, "NAME")

                # Skip this country if it is not for a country in the list ...
                if neName not in territories[territory]["countries"]:
                    continue

                # Loop over Polygons ...
                for poly in pyguymer3.geo.extract_polys(
                    record.geometry,
                    onlyValid = onlyValid,
                       repair = repair,
                ):
                    # Loop over coordinates in exterior ring ...
                    for coord in poly.exterior.coords:
                        # Extract coordinate and add to list ...
                        # NOTE: The BAT is a special case as not all of the
                        #       shape is a BOT.
                        lon, lat = coord                                        # [°], [°]
                        if territory == "British Antarctic Territory":
                            if -80.0 <= lon <= -20.0:
                                territories[territory]["coords"].append((lon, lat))
                        else:
                            territories[territory]["coords"].append((lon, lat))

        # Check if locations are defined ...
        if "locations" in territories[territory]:
            # Loop over locations ...
            for loc in territories[territory]["locations"]:
                # Add to the list ...
                territories[territory]["coords"].append((loc[0], loc[1]))

    # Save database ...
    with open(dbpath, "wt", encoding = "utf-8") as fObj:
        json.dump(
            territories,
            fObj,
            ensure_ascii = False,
                  indent = 4,
               sort_keys = True,
        )
