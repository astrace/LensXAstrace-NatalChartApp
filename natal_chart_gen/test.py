from PIL import Image
from datetime import datetime, timedelta
import os
import pytz
import random
random.seed(111)

import swisseph as swe

from prototype import Planet, Natal_Chart, _generate, random_asset
from constants import PLANET_NAMES, SIGNS, BG_IMG_FILES, IMG_DIR

load_image = lambda filename: Image.open(os.path.join(IMG_DIR, filename))

def create_mock_natal_chart(positions):
    """
    Generates a NatalChart **data object**, and returns it.

    Args:
        positions (list): A list of integer positions representing the planetary positions,
                          starting with the Ascendant.

    Returns:
        Natal_Chart: A Natal Chart Object
    """
    assert len(positions) == len(Natal_Chart.required_objects)

    planets = []
    #Get all the names of planets and celestial objects.
    obj_names = ['Asc', 'Mc'] + list(PLANET_NAMES.keys())
    for name, pos in zip(obj_names, positions):
        sign = SIGNS[int(pos) // 30]
        planets.append(Planet(name, pos % 30, pos, sign))

    return Natal_Chart(planets)


def test_stelliums():
    # generate n stelliums

    def _generate_stellium(n):
        """
            Inner function that generates a Natal Chart with a stellium of `n` randomly positioned planets.

            Args: n (int): The number of planets in the stellium.

            Returns: Natal_Chart: A mock Natal Chart object with a stellium of `n` randomly positioned planets.
        """
        theta = random.uniform(0, 360)
        positions = [random.uniform(theta - 4, theta + 4) for _ in range(n)]
        m = len(Natal_Chart.required_objects) - n
        positions += [random.uniform(0, 360) for _ in range(m)]
        return create_mock_natal_chart(positions)

    for _ in range(10):
        """
          generate conjunction/stellium with x planets,
          where x is randomly chosen between 2 and number of possible objects.
        """
        chart = _generate_stellium(random.randint(2, len(Natal_Chart.required_objects)))
        im = _generate(chart, load_image)
        im.show()

def test_random_asset():
    """
        In this test, we run random_asset X times, and tally the number of times we get each result.
        The purpose here is to ensure that our share of trials for each item matches our probabilities.
    """
    binning_dict = {}
    for name in BG_IMG_FILES.keys():
        binning_dict[name] = 0
    
    print(binning_dict)

    for _ in range(2000001):
       binning_dict[random_asset(BG_IMG_FILES)] += 1

    #Normalize our binning dict, converting to decimal values.
    for item in BG_IMG_FILES.keys():
        binning_dict[item] /= 2000000
    print(binning_dict)

def test_all_bg_images():
    """
    Generate a random natal chart for each background image.
    """
    bg_images = os.listdir("./assets/images/backgrounds")
    for bg_im_file in bg_images:
        chart = random_chart()
        im = _generate(chart, load_image, bg_im_file)
        im.show()

def random_chart():
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

    return Natal_Chart(planets, jd)

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


if __name__ == "__main__":
    #test_stelliums()
    #test_random_asset()
    test_all_bg_images()

