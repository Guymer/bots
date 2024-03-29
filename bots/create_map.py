#!/usr/bin/env python3

# Define function ...
def create_map(name, territory, fpath, /):
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
    """

    # Import standard modules ...
    import os

    # Import special modules ...
    try:
        import cartopy
        cartopy.config.update(
            {
                "cache_dir" : os.path.expanduser("~/.local/share/cartopy_cache"),
            }
        )
    except:
        raise Exception("\"cartopy\" is not installed; run \"pip install --user Cartopy\"") from None
    try:
        import matplotlib
        matplotlib.rcParams.update(
            {
                       "backend" : "Agg",                                       # NOTE: See https://matplotlib.org/stable/gallery/user_interfaces/canvasagg.html
                    "figure.dpi" : 300,
                "figure.figsize" : (9.6, 7.2),                                  # NOTE: See https://github.com/Guymer/misc/blob/main/README.md#matplotlib-figure-sizes
                     "font.size" : 8,
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
        raise Exception("\"pyguymer3\" is not installed; you need to have the Python module from https://github.com/Guymer/PyGuymer3 located somewhere in your $PYTHONPATH") from None

    # Find file containing all the country shapes ...
    sfile = cartopy.io.shapereader.natural_earth(
        resolution = "10m",
          category = "cultural",
              name = "admin_0_countries",
    )

    print(f"Creating map for \"{name}\" ...")

    # NOTE: The strategy here is to find the bounding boxes of all of the shapes
    #       and locations. Now that the region-of-interest is known the large
    #       field-of-view subplot can be centred correctly and the narrow
    #       field-of-view subplot can have the correct extent. Each subplot has
    #       the same data drawn on it.

    # Create empty lists ...
    lon_cen = numpy.empty((0), dtype = numpy.float64)                           # [°]
    lon_cor = numpy.empty((0), dtype = numpy.float64)                           # [°]
    lat_cen = numpy.empty((0), dtype = numpy.float64)                           # [°]
    lat_cor = numpy.empty((0), dtype = numpy.float64)                           # [°]

    # Check if countries are defined ...
    if "countries" in territory:
        # Loop over records ...
        for record in cartopy.io.shapereader.Reader(sfile).records():
            # Create short-hand ...
            neName = pyguymer3.geo.getRecordAttribute(record, "NAME")

            # Skip this country if it is not for a country in the list ...
            if neName not in territory["countries"]:
                continue

            # Find the bounding box ...
            lon1, lat1, lon2, lat2 = record.bounds                              # [°], [°], [°], [°]

            # Add corners to the lists ...
            lon_cor = numpy.append(lon_cor, lon1)                               # [°]
            lon_cor = numpy.append(lon_cor, lon2)                               # [°]
            lat_cor = numpy.append(lat_cor, lat1)                               # [°]
            lat_cor = numpy.append(lat_cor, lat2)                               # [°]

            # Add centroid to the list ...
            lon_cen = numpy.append(lon_cen, 0.5 * (lon1 + lon2))                # [°]
            lat_cen = numpy.append(lat_cen, 0.5 * (lat1 + lat2))                # [°]

    # Check if locations are defined ...
    if "locations" in territory:
        # Loop over locations ...
        for loc in territory["locations"]:
            # Add to the list ...
            lon_cor = numpy.append(lon_cor, loc[0])                             # [°]
            lat_cor = numpy.append(lat_cor, loc[1])                             # [°]
            lon_cen = numpy.append(lon_cen, loc[0])                             # [°]
            lat_cen = numpy.append(lat_cen, loc[1])                             # [°]

    # Check that some points were found ...
    if lon_cor.size == 0 or lat_cor.size == 0 or lon_cen.size == 0 or lat_cen.size == 0:
        raise Exception(f"no points were found for \"{name}\"") from None

    # Create short-hands ...
    pointLon = lon_cen.mean()                                                   # [°]
    pointLat = lat_cen.mean()                                                   # [°]

    # Find the maximum distance of any corner from the centre ...
    maxDist = 0.0                                                               # [m]
    for iCor in range(lat_cor.size):
        maxDist = max(
            maxDist,
            pyguymer3.geo.calc_dist_between_two_locs(
                pointLon,
                pointLat,
                lon_cor[iCor],
                lat_cor[iCor],
            )[0],
        )                                                                       # [m]

    # Create plot ...
    fg = matplotlib.pyplot.figure(figsize = (12.8, 7.2))

    # Create axis ...
    ax1 = fg.add_subplot(
        1,
        2,
        1,
        projection = cartopy.crs.Orthographic(
            central_longitude = pointLon,
             central_latitude = pointLat,
        ),
    )

    # Configure axis ...
    ax1.set_global()
    pyguymer3.geo.add_coastlines(ax1)
    pyguymer3.geo.add_map_background(ax1, resolution = "large8192px")

    # Check if countries are defined ...
    if "countries" in territory:
        # Loop over records ...
        for record in cartopy.io.shapereader.Reader(sfile).records():
            # Create short-hand ...
            neName = pyguymer3.geo.getRecordAttribute(record, "NAME")

            # Skip this record if it is not for a country in the list ...
            if neName not in territory["countries"]:
                continue

            # Add areas to plot ...
            ax1.add_geometries(
                pyguymer3.geo.extract_polys(record.geometry),
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
            # Add location to plot ...
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

    # Create axis ...
    ax2 = pyguymer3.geo.add_top_down_axis(
        fg,
        pointLon,
        pointLat,
        maxDist + 12.0 * 1852.0,
        nrows = 1,
        ncols = 2,
        index = 2,
    )

    # Configure axis ...
    pyguymer3.geo.add_coastlines(ax2)
    pyguymer3.geo.add_map_background(ax2, resolution = "large8192px")

    # Check if countries are defined ...
    if "countries" in territory:
        # Loop over records ...
        for record in cartopy.io.shapereader.Reader(sfile).records():
            # Create short-hand ...
            neName = pyguymer3.geo.getRecordAttribute(record, "NAME")

            # Skip this record if it is not for a country in the list ...
            if neName not in territory["countries"]:
                continue

            # Add areas to plot ...
            ax2.add_geometries(
                pyguymer3.geo.extract_polys(record.geometry),
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
            # Add location to plot ...
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
    pyguymer3.image.optimize_image(
        fpath,
        strip = True,
    )
