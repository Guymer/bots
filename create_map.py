def create_map(name, territory, fpath):
    # Import special modules ...
    try:
        import cartopy
        import cartopy.io
        import cartopy.io.shapereader
    except:
        raise Exception("\"cartopy\" is not installed; run \"pip install --user Cartopy\"") from None
    try:
        import matplotlib
        matplotlib.use("Agg")                                                   # NOTE: See https://matplotlib.org/stable/gallery/user_interfaces/canvasagg.html
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
    shape_file = cartopy.io.shapereader.natural_earth(
        resolution = "10m",
        category = "cultural",
        name = "admin_0_countries"
    )

    print("Creating map for \"{:s}\" ...".format(name))

    # NOTE: The strategy here is to find the bounding boxes of all of the shapes
    #       and locations. Now that the region-of-interest is known the large
    #       field-of-view subplot can be centred correctly and the narrow
    #       field-of-view subplot can have the correct extent. Each subplot has
    #       the same data drawn on it.

    # Create empty lists ...
    lon_avg = numpy.empty((0), dtype = numpy.float64)
    lon_cor = numpy.empty((0), dtype = numpy.float64)
    lat_avg = numpy.empty((0), dtype = numpy.float64)
    lat_cor = numpy.empty((0), dtype = numpy.float64)

    # Check if countries are defined ...
    if "countries" in territory:
        # Loop over records ...
        for record in cartopy.io.shapereader.Reader(shape_file).records():
            # Skip this record if it is not for a country in the list ...
            if record.attributes["NAME"] not in territory["countries"]:
                continue

            # Find the bounding box ...
            lon1, lat1, lon2, lat2 = record.bounds

            # Add corners to the lists ...
            lon_cor = numpy.append(lon_cor, lon1)
            lon_cor = numpy.append(lon_cor, lon2)
            lat_cor = numpy.append(lat_cor, lat1)
            lat_cor = numpy.append(lat_cor, lat2)

            # Add middle to the list ...
            lon_avg = numpy.append(lon_avg, 0.5 * (lon1 + lon2))
            lat_avg = numpy.append(lat_avg, 0.5 * (lat1 + lat2))

    # Check if locations are defined ...
    if "locations" in territory:
        # Loop over locations ...
        for loc in territory["locations"]:
            # Add to the list ...
            lon_cor = numpy.append(lon_cor, loc[0])
            lat_cor = numpy.append(lat_cor, loc[1])
            lon_avg = numpy.append(lon_avg, loc[0])
            lat_avg = numpy.append(lat_avg, loc[1])

    # Check that some points were found ...
    if lon_cor.size == 0 or lat_cor.size == 0 or lon_avg.size == 0 or lat_avg.size == 0:
        raise Exception("no points were found for \"{:s}\"".format(name)) from None

    # Create plot ...
    fg = matplotlib.pyplot.figure(figsize = (6, 3), dpi = 300)

    # Create first subplot ...
    ax1 = matplotlib.pyplot.subplot(
        1,
        2,
        1,
        projection = cartopy.crs.Orthographic(
            central_longitude = lon_avg.mean(),
             central_latitude = lat_avg.mean()
        )
    )
    ax1.set_global()
    pyguymer3.geo.add_map_background(ax1, resolution = "large4096px")
    ax1.coastlines(resolution = "10m", color = "black", linewidth = 0.1)

    # Check if countries are defined ...
    if "countries" in territory:
        # Loop over records ...
        for record in cartopy.io.shapereader.Reader(shape_file).records():
            # Skip this record if it is not for a country in the list ...
            if record.attributes["NAME"] not in territory["countries"]:
                continue

            # Add areas to plot ...
            ax1.add_geometries(
                record.geometry,
                cartopy.crs.PlateCarree(),
                alpha = 0.5,
                color = "red",
                facecolor = "red",
                linewidth = 0.1
            )

    # Check if locations are defined ...
    if "locations" in territory:
        # Loop over locations ...
        for loc in territory["locations"]:
            # Add location to plot ...
            matplotlib.pyplot.plot(
                loc[0],
                loc[1],
                transform = cartopy.crs.Geodetic(),
                linestyle = "None",
                marker = "o",
                markersize = 2.0,
                color = "red",
                antialiased = True
            )

    # Create second subplot ...
    ax2 = matplotlib.pyplot.subplot(
        1,
        2,
        2,
        projection = cartopy.crs.PlateCarree()
    )
    ax2.set_extent(
        [
            lon_cor.min() - 1.0,
            lon_cor.max() + 1.0,
            lat_cor.min() - 1.0,
            lat_cor.max() + 1.0
        ]
    )
    pyguymer3.geo.add_map_background(ax2, resolution = "large4096px")
    ax2.coastlines(resolution = "10m", color = "black", linewidth = 0.1)

    # Check if countries are defined ...
    if "countries" in territory:
        # Loop over records ...
        for record in cartopy.io.shapereader.Reader(shape_file).records():
            # Skip this record if it is not for a country in the list ...
            if record.attributes["NAME"] not in territory["countries"]:
                continue

            # Add areas to plot ...
            ax2.add_geometries(
                record.geometry,
                cartopy.crs.PlateCarree(),
                alpha = 0.5,
                color = "red",
                facecolor = "red",
                linewidth = 0.1
            )

    # Check if locations are defined ...
    if "locations" in territory:
        # Loop over locations ...
        for loc in territory["locations"]:
            # Add location to plot ...
            matplotlib.pyplot.plot(
                loc[0],
                loc[1],
                transform = cartopy.crs.Geodetic(),
                linestyle = "None",
                marker = "o",
                markersize = 2.0,
                color = "red",
                antialiased = True
            )

    # Save plot ...
    fg.suptitle(name)
    fg.savefig(
        fpath,
        bbox_inches = "tight",
                dpi = 300,
         pad_inches = 0.1
    )
    pyguymer3.image.optimize_image(fpath, strip = True)
    matplotlib.pyplot.close(fg)
