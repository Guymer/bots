# -*- coding: utf-8 -*-

def create_map(name, territory, fpath):
    # Import modules ...
    import cartopy
    import cartopy.io
    import cartopy.io.shapereader
    import matplotlib
    # NOTE: http://matplotlib.org/faq/howto_faq.html#matplotlib-in-a-web-application-server
    matplotlib.use("Agg")
    import matplotlib.pyplot
    import numpy
    import pyguymer

    # Find file containing all the country shapes ...
    shape_file = cartopy.io.shapereader.natural_earth(
        resolution = "10m",
        category = "cultural",
        name = "admin_0_countries"
    )

    print u"Creating map for \"{0:s}\" ...".format(name)

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

    # Create plot ...
    fig = matplotlib.pyplot.figure(
        figsize = (6, 3),
        dpi = 300,
        frameon = False
    )

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
    pyguymer.add_map_background(ax1, resolution = "large4096px")
    ax1.coastlines(
        resolution = "10m",
        color = "black",
        linewidth = 0.1
    )

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
    pyguymer.add_map_background(ax2, resolution = "large4096px")
    ax2.coastlines(
        resolution = "10m",
        color = "black",
        linewidth = 0.1
    )

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
    matplotlib.pyplot.title(
        name,
        size = "small"
    )
    matplotlib.pyplot.savefig(
        fpath,
        bbox_inches = "tight",
        dpi = 300,
        pad_inches = 0.1
    )
    matplotlib.pyplot.close("all")
