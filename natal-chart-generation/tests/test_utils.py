from datetime import datetime, timedelta
import random
import sys
import pytz
import swisseph as swe

from constants import EPHE_DIR, PLANET_NAMES, SIGNS
from natal_chart import NatalChart, Planet

swe.set_ephe_path('../' + EPHE_DIR)

def generate_stellium(n):
    """
        Generate a Natal Chart with a stellium of `n` randomly positioned planets.
        Args: n (int): The number of planets in the stellium.
        Returns: NatalChart: A mock Natal Chart object with a stellium of `n` randomly positioned planets.
    """
    theta = random.uniform(0, 360)
    positions = [random.uniform(theta - 4, theta + 4) for _ in range(n)]
    m = len(NatalChart.required_objects) - n
    positions += [random.uniform(0, 360) for _ in range(m)]
    return create_mock_natal_chart(positions)

def generate_stellium_near_zero_degrees(n):
    """
    Generate a Natal Chart with a stellium of `n` planets, where the planetary positions in the stellium
    are close to the boundary of a circle's circumference (i.e., between 356-360 and 0-4 degrees).

    Note:
        This edge case needs to be tested to make sure the `find_clumps` and `spread_planets` algos
        work in this case.

    Args:
        n (int): The number of planets in the stellium.
    Returns:
        NatalChart: A mock Natal Chart object with a stellium of `n` planets, with positions near the boundary
                     of a circle's circumference.
    """
    # Select a random degree between 356-360 or 0-4
    def _random_theta():
        if random.randint(0, 1):
            return random.uniform(356, 360)
        else:
            return random.uniform(0, 4)

    positions = [_random_theta() for _ in range(n)]
    m = len(NatalChart.required_objects) - n
    positions += [random.uniform(0, 360) for _ in range(m)]
    return create_mock_natal_chart(positions)

def create_mock_natal_chart(positions):
    """
    Generates a NatalChart object.
    Args:
        positions (list): A list of integer positions representing the planetary positions,
                          starting with the Ascendant.
    Returns:
        NatalChart: A Natal Chart Object
    """
    assert len(positions) == len(NatalChart.required_objects)

    planets = []
    #Get all the names of planets and celestial objects.
    obj_names = list(NatalChart.required_objects)
    for name, pos in zip(obj_names, positions):
        sign = SIGNS[int(pos) // 30]
        planets.append(Planet(name, pos % 30, pos, sign))

    return NatalChart(planets)

def random_chart():
    """
    Generates a random NatalChart object based on a random date, time, and location.
    Returns:
        NatalChart: A randomly generated Natal Chart Object
    """
    dt = random_datetime()
    geo = random_location()

    tz = pytz.timezone('UTC')
    dt = dt.astimezone(tz)
    # calculate Julian day
    # requires hour input as decimal with fraction
    hour = dt.hour + (dt.minute + dt.second / 60) / 60
    jd = swe.julday(dt.year, dt.month, dt.day, hour)

    # NOTE: ascendant is very important for orienting entire chart
    _, ascmc = swe.houses(jd, geo[0], geo[1], bytes('W', 'utf-8'))
    asc = SIGNS[int(ascmc[0] // 30)]

    # create planet object/layer list
    planets = []
    for name, no_body in PLANET_NAMES.items():
        abs_pos = swe.calc_ut(jd, no_body)[0][0]
        pos = abs_pos % 30
        sign = SIGNS[int(abs_pos // 30)]
        p = Planet(name, pos, abs_pos, sign)
        planets.append(p)

    # add angles
    for abs_pos, name in [(ascmc[0], 'Asc'), (ascmc[1], 'Mc')]:
        pos = abs_pos % 30
        sign = SIGNS[int(abs_pos // 30)]
        p = Planet(name, pos, abs_pos, sign)
        planets.append(p)

    return NatalChart(planets, jd)

def random_datetime():
    """
    Returns a random datetime object representing a time within the last 2000 years.
    Returns:
        datetime.datetime: A datetime object representing a random time within the last 2000 years.
    """
    now = datetime.now()
    start_date = now - timedelta(days=365 * 100)
    end_date = now
    days_between = (end_date - start_date).days
    random_days = random.randrange(days_between)
    return start_date + timedelta(days=random_days)

def random_location():
    """
    Returns a random longitude and latitude as a tuple.
    Returns:
        tuple: A tuple containing the longitude and latitude values as floats.
    """
    longitude = random.uniform(-180, 180)
    latitude = random.uniform(-90, 90)
    return longitude, latitude
