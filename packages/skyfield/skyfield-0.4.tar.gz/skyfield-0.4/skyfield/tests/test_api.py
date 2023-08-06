"""Basic tests of the Skyfield API module and its contents."""

import assay
from skyfield import api
from skyfield import positionlib

def test_whether_planets_have_radii():
    assert api.mercury.radius.km == 2440.0
    for planet in api.nine_planets:
        assert planet.radius.km > 0.0

def test_sending_jd_that_is_not_a_julian_date():
    with assay.raises(ValueError, 'your "jd" argument is not a JulianDate: '):
        api.earth('blah')

def test_apparent_position_class():
    p = api.earth(utc=(2014, 2, 9, 14, 50)).observe(api.mars).apparent()
    assert isinstance(p, positionlib.Apparent)

def test_astrometric_position_class():
    p = api.earth(utc=(2014, 2, 9, 14, 50)).observe(api.mars)
    assert isinstance(p, positionlib.Astrometric)

def test_planet_position_class():
    p = api.mars(utc=(2014, 2, 9, 14, 50))
    assert isinstance(p, positionlib.Barycentric)

def test_star_position_class():
    star = api.Star(ra_hours=0, dec_degrees=0)
    p = api.earth(utc=(2014, 2, 9, 15, 1)).observe(star)
    assert isinstance(p, positionlib.Astrometric)
