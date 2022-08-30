def create_db(dbpath):
    # Import standard modules ...
    import json

    # Import special modules ...
    try:
        import cartopy
        import cartopy.io
        import cartopy.io.shapereader
    except:
        raise Exception("\"cartopy\" is not installed; run \"pip install --user Cartopy\"") from None

    # Import my modules ...
    try:
        import pyguymer3
        import pyguymer3.geo
    except:
        raise Exception("\"pyguymer3\" is not installed; you need to have the Python module from https://github.com/Guymer/PyGuymer3 located somewhere in your $PYTHONPATH") from None

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
    shape_file = cartopy.io.shapereader.natural_earth(
        resolution = "10m",
          category = "cultural",
              name = "admin_0_countries",
    )

    # Loop over territories ...
    for territory in territories:
        print(f"Finding locations for \"{territory}\" ...")

        # Create empty list ...
        territories[territory]["coords"] = []

        # Check if countries are defined ...
        if "countries" in territories[territory]:
            # Loop over records ...
            for record in cartopy.io.shapereader.Reader(shape_file).records():
                # Create short-hands ...
                # NOTE: According to the developer of Natural Earth:
                #           "Because Natural Earth has a more fidelity than ISO,
                #           and tracks countries that ISO doesn't, Natural Earth
                #           maintains it's own set of 3-character codes for each
                #           admin-0 related feature."
                #       Therefore, when "ISO_A2" or "ISO_A3" are not populated I
                #       must fall back on "ISO_A2_EH" and "ISO_A3_EH" instead,
                #       see:
                #         * https://github.com/nvkelso/natural-earth-vector/issues/268
                neA2 = record.attributes["ISO_A2"].replace("\x00", " ").strip()
                neA3 = record.attributes["ISO_A3"].replace("\x00", " ").strip()
                neCountry = record.attributes["NAME"].replace("\x00", " ").strip()
                if neA2 == "-99":
                    print(f"INFO: Falling back on \"ISO_A2_EH\" for \"{neCountry}\".")
                    neA2 = record.attributes["ISO_A2_EH"].replace("\x00", " ").strip()
                if neA3 == "-99":
                    print(f"INFO: Falling back on \"ISO_A3_EH\" for \"{neCountry}\".")
                    neA3 = record.attributes["ISO_A3_EH"].replace("\x00", " ").strip()

                # Skip this country if it is not for a country in the list ...
                if neCountry not in territories[territory]["countries"]:
                    continue

                # Loop over boundaries ...
                for boundary in pyguymer3.geo.extract_lines(record.geometry.boundary):
                    # Loop over coordinates ...
                    for coord in boundary.coords:
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
    with open(dbpath, "wt", encoding = "utf-8") as fobj:
        json.dump(
            territories,
            fobj,
            ensure_ascii = False,
                  indent = 4,
               sort_keys = True,
        )
