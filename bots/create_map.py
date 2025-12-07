#!/usr/bin/env python3

# Define function ...
def create_map(
    name,
    territory,
    fpath,
    /,
    *,
        debug = __debug__,
        nIter = 100,
    onlyValid = False,
       repair = False,
      timeout = 60.0,
):
    """Create a map of a territory

    This function creates a PNG map of all of the countries in a territory.

    Parameters
    ----------
    name : str
        the name of the territory
    territory : dict
        the database entry for the territory
    fpath : str
        the path to save the PNG
    debug : bool, optional
        print debug messages
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
    import os
    import pathlib

    # Import special modules ...
    try:
        import cartopy
        cartopy.config.update(
            {
                "cache_dir" : pathlib.PosixPath("~/.local/share/cartopy").expanduser(),
            }
        )
    except:
        raise Exception("\"cartopy\" is not installed; run \"pip install --user Cartopy\"") from None
    try:
        import matplotlib
        matplotlib.rcParams.update(
            {
                            "backend" : "Agg",                                  # NOTE: See https://matplotlib.org/stable/gallery/user_interfaces/canvasagg.html
                         "figure.dpi" : 300,
                     "figure.figsize" : (9.6, 7.2),                             # NOTE: See https://github.com/Guymer/misc/blob/main/README.md#matplotlib-figure-sizes
                          "font.size" : 8,
                "image.interpolation" : "none",
                     "image.resample" : False,
            }
        )
        import matplotlib.pyplot
    except:
        raise Exception("\"matplotlib\" is not installed; run \"pip install --user matplotlib\"") from None
    try:
        import numpy
    except:
        raise Exception("\"numpy\" is not installed; run \"pip install --user numpy\"") from None

    # Import my modules ...
    try:
        import pyguymer3
        import pyguymer3.geo
        import pyguymer3.image
    except:
        raise Exception("\"pyguymer3\" is not installed; run \"pip install --user PyGuymer3\"") from None

    # Find file containing all the country shapes ...
    sfile = cartopy.io.shapereader.natural_earth(
        resolution = "10m",
          category = "cultural",
              name = "admin_0_countries",
    )

    print(f"Creating map for \"{name}\" ...")

    # Create empty lists ...
    lons = numpy.empty((0), dtype = numpy.float64)                              # [°]
    lats = numpy.empty((0), dtype = numpy.float64)                              # [°]

    # Check if countries are defined ...
    if "countries" in territory:
        # Loop over records ...
        for record in cartopy.io.shapereader.Reader(sfile).records():
            # Create short-hand ...
            neName = pyguymer3.geo.getRecordAttribute(record, "NAME")

            # Skip this country if it is not for a country in the list ...
            if neName not in territory["countries"]:
                continue

            # Loop over Polygons ...
            for poly in pyguymer3.geo.extract_polys(
                record.geometry,
                onlyValid = onlyValid,
                   repair = repair,
            ):
                # Convert the CoordinateSequence of the exterior LinearRing to a
                # NumPy array ...
                points = numpy.array(poly.exterior.coords)                      # [°]

                # Add points to lists ...
                lons = numpy.concatenate((lons, points[:, 0]))                  # [°]
                lats = numpy.concatenate((lats, points[:, 1]))                  # [°]

    # Check if locations are defined ...
    if "locations" in territory:
        # Loop over locations ...
        for loc in territory["locations"]:
            # Add points to lists ...
            lons = numpy.append(lons, loc[0])                                   # [°]
            lats = numpy.append(lats, loc[1])                                   # [°]

    # Check that some points were found ...
    if lons.size == 0 or lats.size == 0:
        raise Exception(f"no points were found for \"{name}\"") from None

    # Find the middle of the points ...
    midLon, midLat, maxDist = pyguymer3.geo.find_middle_of_locs(
        lons,
        lats,
         angConv = 0.1,
            conv = 10000.0,                                                     # 10 km
           debug = debug,
          method = "GeodesicCircle",
            nAng = 9,
           nIter = nIter,
         nRefine = 6,                                                           # 156.25 m
             pad = 12.0 * 1852.0,
        useSciPy = False,
    )                                                                           # [°], [°], [m]

    # Create plot ...
    fg = matplotlib.pyplot.figure(figsize = (12.8, 7.2))

    # Create axes ...
    ax1 = pyguymer3.geo.add_axis(
        fg,
        add_coastlines = True,
         add_gridlines = True,
                 debug = debug,
                 index = 1,
                   lat = midLat,
                   lon = midLon,
                 ncols = 2,
                 nIter = nIter,
                 nrows = 1,
             onlyValid = onlyValid,
                repair = repair,
    )
    ax2 = pyguymer3.geo.add_axis(
        fg,
          add_coastlines = True,
           add_gridlines = True,
                   debug = debug,
                    dist = maxDist,
                   index = 2,
                     lat = midLat,
                     lon = midLon,
                   ncols = 2,
                   nIter = nIter,
                   nrows = 1,
               onlyValid = onlyValid,
                  repair = repair,
        satellite_height = False,
    )

    # Configure axes ...
    pyguymer3.geo.add_map_background(
        ax1,
             debug = debug,
        resolution = "large0512px",
    )
    pyguymer3.geo.add_map_background(
        ax2,
             debug = debug,
        resolution = "large8192px",
    )

    # Check if countries are defined ...
    if "countries" in territory:
        # Loop over records ...
        for record in cartopy.io.shapereader.Reader(sfile).records():
            # Create short-hand ...
            neName = pyguymer3.geo.getRecordAttribute(record, "NAME")

            # Skip this record if it is not for a country in the list ...
            if neName not in territory["countries"]:
                continue

            # Add Polygons to axes ...
            ax1.add_geometries(
                pyguymer3.geo.extract_polys(
                    record.geometry,
                    onlyValid = onlyValid,
                       repair = repair,
                ),
                cartopy.crs.PlateCarree(),
                    alpha = 0.5,
                    color = "red",
                facecolor = "red",
                linewidth = 0.1,
            )
            ax2.add_geometries(
                pyguymer3.geo.extract_polys(
                    record.geometry,
                    onlyValid = onlyValid,
                       repair = repair,
                ),
                cartopy.crs.PlateCarree(),
                    alpha = 0.5,
                    color = "red",
                facecolor = "red",
                linewidth = 0.1,
            )

    # Check if locations are defined ...
    if "locations" in territory:
        # Loop over locations ...
        for loc in territory["locations"]:
            # Add location to axes ...
            ax1.plot(
                loc[0],
                loc[1],
                  transform = cartopy.crs.Geodetic(),
                  linestyle = "None",
                     marker = "o",
                 markersize = 2.0,
                      color = "red",
                antialiased = True,
            )
            ax2.plot(
                loc[0],
                loc[1],
                  transform = cartopy.crs.Geodetic(),
                  linestyle = "None",
                     marker = "o",
                 markersize = 2.0,
                      color = "red",
                antialiased = True,
            )

    # Configure figure ...
    fg.suptitle(name)
    fg.tight_layout()

    # Save figure ...
    fg.savefig(fpath)
    matplotlib.pyplot.close(fg)

    # Optimize PNG ...
    pyguymer3.image.optimise_image(
        fpath,
          debug = debug,
          strip = True,
        timeout = timeout,
    )
