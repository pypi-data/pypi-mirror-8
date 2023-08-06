
==================
 Earth Satellites
==================

.. currentmodule:: skyfield

The orbital elements for human-launched Earth satellites
can go out of date in only a few days,
so it is best to start a programming or analysis session
by downloading fresh orbital elements for your object of interest
from the
`NORAD Two-Line Element Sets <http://celestrak.com/NORAD/elements/>`_
(TLE) page of the Celestrak web site.

Once you have acquired the two-line orbital elements,
simply read them from a file or paste them directly into your script
to find out whether a satellite is above your local horizon:

.. testcode::

    text = """
    ISS (ZARYA)             
    1 25544U 98067A   14020.93268519  .00009878  00000-0  18200-3 0  5082
    2 25544  51.6498 109.4756 0003572  55.9686 274.8005 15.49815350868473
    """

    from skyfield.api import JulianDate, earth

    bluffton = earth.topos('40.8939 N', '83.8917 W')
    tup = (2014, 1, 21, 11, 18, 7)

    sat = earth.satellite(text)
    alt, az, distance = bluffton(utc=tup).observe(sat).altaz()

    print(alt)
    print(az)
    print(distance.km)

.. testoutput::

    13deg 49' 57.8"
    357deg 51' 21.8"
    1281.20477925

Beware: the two-line element format is very rigid.
The meaning of each character
is based on its exact offset from the beginning of the line —
so you must download and use the element set’s text
without making any change to its whitespace.

The standard SGP4 theory of satellite motion that Skyfield uses
is a rough enough model of the near-Earth environment
that it can only predict a satellite position
to within an accuracy of a few kilometers.
This error grows larger as a TLE element set becomes several weeks old,
until its predictions are no longer meaningful.

Propagation Errors
==================

After building a satellite object,
you can examine the *epoch* date and time
when the TLE element set’s predictions are most accurate.
The ``epoch`` attribute is a :class:`JulianDate`,
so it supports all of the standard Skyfield date methods:

.. testcode::

    text = """
    GOCE                    
    1 34602U 09013A   13314.96046236  .14220718  20669-5  50412-4 0   930
    2 34602 096.5717 344.5256 0009826 296.2811 064.0942 16.58673376272979
    """
    sat = earth.satellite(text)
    print(sat.epoch.utc_jpl())

.. testoutput::

    A.D. 2013-Nov-09 23:03:03.9479 UT

Skyfield is willing to generate positions
for dates quite far from a satellite’s epoch,
even if they are not likely to be meaningful.
But it cannot generate a position
beyond the point where the elements stop making physical sense.
At that point, the satellite will return a position and velocity
``(nan, nan, nan)`` where all of the quantities
are the special floating-point value ``nan`` which means *not-a-number*.

When a propagation error occurs and you get ``nan`` values,
you can examine the ``sgp4_error`` attribute of the returned position
to learn the error that the SGP4 propagator encountered.

We can take as an example the satellite elements above.
They are the last elements ever issued for GOCE,
about one day before the satellite re-entered the atmosphere
after an extended and successful mission.
Because of the steep decay of its orbit,
the elements are valid over an unusually short period —
from just before noon on Saturday to just past noon on Tuesday:

.. image:: _static/goce-decay.png

By asking for GOCE’s position just before or after this window,
we can learn about the propagation errors
that are limiting this TLE set’s predictions:

.. testcode::

    geocentric = sat.gcrs(utc=(2013, 11, 9))
    print('Before:')
    print(geocentric.position.km)
    print(geocentric.sgp4_error)

    geocentric = sat.gcrs(utc=(2013, 11, 13))
    print('\nAfter:')
    print(geocentric.position.km)
    print(geocentric.sgp4_error)

.. testoutput::

    Before:
    [ nan  nan  nan]
    mean eccentricity -0.001416 not within range 0.0 <= e < 1.0

    After:
    [ nan  nan  nan]
    mrt 0.997178 is less than 1.0 indicating the satellite has decayed

If you use a Julian date array to ask about an entire range of dates,
then ``sgp4_error`` will be a sequence filled in with ``None``
whenever the SGP4 propagator was successful
and otherwise recording the propagator error:

.. testcode::

    from pprint import pprint

    geocentric = sat.gcrs(utc=(2013, 11, [9, 10, 11, 12, 13]))
    pprint(geocentric.sgp4_error)

.. testoutput::

    ['mean eccentricity -0.001416 not within range 0.0 <= e < 1.0',
     None,
     None,
     None,
     'mrt 0.997178 is less than 1.0 indicating the satellite has decayed']


