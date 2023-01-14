#!/usr/bin/env python3

# Define function ...
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
        matplotlib.pyplot.rcParams.update({"font.size" : 8})
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

    # Create plot ...
    fg = matplotlib.pyplot.figure(
            dpi = 300,
        figsize = (6, 3),
    )

    # Create axes ...
    ax1 = fg.add_subplot(
        1,
        2,
        1,
        projection = cartopy.crs.Orthographic(
            central_longitude = lon_cen.mean(),
             central_latitude = lat_cen.mean(),
        ),
    )
    ax1.set_global()
    pyguymer3.geo.add_map_background(ax1, resolution = "large8192px")
    ax1.coastlines(resolution = "10m", color = "black", linewidth = 0.1)

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
    ax2 = fg.add_subplot(
        1,
        2,
        2,
        projection = cartopy.crs.Orthographic(
            central_longitude = lon_cen.mean(),
             central_latitude = lat_cen.mean(),
        ),
    )
    ax2.set_extent(
        [
            max(-180.0, lon_cor.min() - 1.0),
            min( 180.0, lon_cor.max() + 1.0),
            max( -90.0, lat_cor.min() - 1.0),
            min(  90.0, lat_cor.max() + 1.0),
        ]
    )
    pyguymer3.geo.add_map_background(ax2, resolution = "large8192px")
    ax2.coastlines(resolution = "10m", color = "black", linewidth = 0.1)

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
    fg.savefig(
        fpath,
               dpi = 300,
        pad_inches = 0.1,
    )
    matplotlib.pyplot.close(fg)

    # Optimize PNG ...
    pyguymer3.image.optimize_image(
        fpath,
        strip = True,
    )
