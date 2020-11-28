def create_timeline(dirOut, territories, n = 10):
    # Import standard modules ...
    import calendar
    import datetime
    import os

    # Import special modules ...
    try:
        import ephem
    except:
        raise Exception("\"ephem\" is not installed; run \"pip install --user ephem\"") from None
    try:
        import matplotlib
        matplotlib.use("Agg")                                                   # NOTE: https://matplotlib.org/gallery/user_interfaces/canvasagg.html
        import matplotlib.dates
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
    except:
        raise Exception("\"pyguymer3\" is not installed; you need to have the Python module from https://github.com/Guymer/PyGuymer3 located somewhere in your $PYTHONPATH") from None

    # Create plot ...
    fg = matplotlib.pyplot.figure(figsize = (12, 6), dpi = 300)
    ax = matplotlib.pyplot.subplot()
    ax.xaxis_date()
    ax.xaxis.grid(True)

    # Create observer ...
    obs = ephem.Observer()

    # Set counter ...
    j = 0

    # Loop over territories ...
    for territory in territories.keys():
        print("Finding sunrises and sunsets for \"{:s}\" ...".format(territory))

        # Create start date ...
        d0 = ephem.Date((2016, 10, 14, 0, 0, 0))

        # Create empty lists ...
        risMins = numpy.zeros(n, dtype = numpy.uint64)                          # [s]
        risMaxs = numpy.zeros(n, dtype = numpy.uint64)                          # [s]
        setMins = numpy.zeros(n, dtype = numpy.uint64)                          # [s]
        setMaxs = numpy.zeros(n, dtype = numpy.uint64)                          # [s]

        # Loop over days ...
        for i in range(n):
            # Initialize counters ...
            risMins[i] = 2 ** 62                                                # [s]
            setMins[i] = 2 ** 62                                                # [s]

            # Loop over coordinates ...
            for coord in territories[territory]["coords"]:
                # Update observer ...
                # HACK: Must be a crude string otherwise it does not set it
                #       correctly.
                obs.long = str(coord[0])
                obs.lat = str(coord[1])

                # Find sunrise and sunset as 'naive' datetime objects in UTC ...
                try:
                    d1 = obs.next_rising(ephem.Sun(), ephem.Date(d0 + i)).datetime()
                except ephem.AlwaysUpError:
                    continue
                try:
                    d2 = obs.next_setting(ephem.Sun(), ephem.Date(d1)).datetime()
                except ephem.AlwaysUpError:
                    continue

                # Convert sunrise and sunset to 'aware' datetime objects in UTC ...
                d1 = d1.replace(tzinfo = datetime.timezone.utc)
                d2 = d2.replace(tzinfo = datetime.timezone.utc)

                # Convert sunrise and sunset to integers since the POSIX epoch ...
                # NOTE: There are many clunky ways of converting a datetime
                #       object into an integer. The neatest way uses
                #       "strftime()" but this is bad for two reasons:
                #         1) it is not supported on Windows; and
                #         2) it ignores the "tzinfo" data.
                #       This last point took over an hour to identify. The
                #       following two threads put me out of my misery:
                #         1) https://stackoverflow.com/a/19801863; and
                #         2) https://bugs.python.org/issue12750#msg142245
                t1 = int(calendar.timegm(d1.timetuple()))                       # [s]
                t2 = int(calendar.timegm(d2.timetuple()))                       # [s]

                # Overwrite counters if needed ...
                risMins[i] = min(t1, risMins[i])                                # [s]
                risMaxs[i] = max(t1, risMaxs[i])                                # [s]
                setMins[i] = min(t2, setMins[i])                                # [s]
                setMaxs[i] = max(t2, setMaxs[i])                                # [s]

        # Convert integers since the POSIX epoch to MatPlotLib dates ...
        # NOTE: Just count how many different kinds the same date is represented
        #       with in this script and try to tell me with a straight face that
        #       it is convenient and efficient.
        x1 = []
        x2 = []
        dx1 = []
        dx2 = []
        for i in range(n):
            x1.append(matplotlib.dates.date2num(datetime.datetime.utcfromtimestamp(risMins[i])))
            x2.append(matplotlib.dates.date2num(datetime.datetime.utcfromtimestamp(risMaxs[i])))
            dx1.append(
                matplotlib.dates.date2num(datetime.datetime.utcfromtimestamp(setMaxs[i])) -
                matplotlib.dates.date2num(datetime.datetime.utcfromtimestamp(risMins[i]))
            )
            dx2.append(
                matplotlib.dates.date2num(datetime.datetime.utcfromtimestamp(setMins[i])) -
                matplotlib.dates.date2num(datetime.datetime.utcfromtimestamp(risMaxs[i]))
            )

        # Plot data ...
        ax.barh(
            numpy.zeros(n, dtype = numpy.float64) + 0.5 + j,
            dx1,
            height = 0.8,
            left = x1,
            align = "center",
            alpha = 0.5,
            color = matplotlib.pyplot.cm.rainbow(float(j) / float(len(territories) - 1)),
            linewidth = 0.1
        )
        ax.barh(
            numpy.zeros(n, dtype = numpy.float64) + 0.5 + j,
            dx2,
            height = 0.8,
            left = x2,
            align = "center",
            color = matplotlib.pyplot.cm.rainbow(float(j) / float(len(territories) - 1)),
            label = territory,
            linewidth = 0.1
        )

        # Increment counter ...
        j += 1

    # Save plot ...
    ax.legend(fontsize = "small")
    ax.set_title("Sunrises and sunsets in the BOT")
    ax.set_xlim(
        matplotlib.dates.date2num(ephem.Date(d0 + 1).datetime()),
        matplotlib.dates.date2num(ephem.Date(d0 + n - 2).datetime())
    )
    ax.set_ylim(0, len(territories))
    ax.set_yticks([], [])
    fg.savefig(
        os.path.join(dirOut, "plot.png"),
        bbox_inches = "tight",
                dpi = 300,
         pad_inches = 0.1
    )
    pyguymer3.optimize_image(os.path.join(dirOut, "plot.png"), strip = True)
    matplotlib.pyplot.close("all")