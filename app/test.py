from PIL import Image
from datetime import datetime, timedelta
import os
import pytz
import random
random.seed(111)

import swisseph as swe

from prototype import Planet, Natal_Chart, _generate
from constants import PLANET_NAMES, SIGNS, IMG_DIR

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

    for _ in range(3):
        """
          generate conjunction/stellium with x planets,
          where x is randomly chosen between 2 and number of possible objects.
        """
        #random.randint(2, len(Natal_Chart.required_objects))
        chart = _generate_stellium(2)
        im = _generate(chart, load_image)
        im.show()

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

def stellium_test_run(int_list):
    """
        Given a list of 13 integer positions for each planet, generate a chart.

        Args:
            - intList: List of Integers that gives the angular position of the planets.

        Notes: No error checking for list. If improper list length occurs,
        code can silently fail in other places (like _generate()).            
    """

    test_chart = create_mock_natal_chart(int_list) #Need 13
    for pname in test_chart.objects.keys():
        print(test_chart.objects[pname])
    im = _generate(test_chart, load_image)
    im.show()

def stellium_test_battery():
    """
        Wrapping function that runs a bunch of tests.
        Speficially, we focus on stelliums (groups) near/on the ascendant boundary.
    """

    #Test1: Our first pathological test:
    stellium_test_run([1,1,8,8,20,20,60,60,100,100,120,120,200])
    #Test2: All planets just separated by 20 degrees, starting from 0
    stellium_test_run([20,40,60,80,100,120,140,160,180,200,220,240,260]) 
    #Test3: Pairs of two, spread out over the perimeter.
    stellium_test_run([10,10,50,50,90,90,130,130,170,170,240,240,300])
    #Test4: Pairs of two, with some pairs straddeling boundary.
    stellium_test_run([5,5,90,90,130,130,170,170,240,240,300,355,355])
    #Test5: Pairs of two, with a pair over boundary.
    #Fails
    stellium_test_run([0,45,90,90,130,130,170,170,240,240,300,345,359])
    #Test6: Group of three, spread out.
    stellium_test_run([40,40,40,120,120,120,200,200,200,250,250,250,320])
    #Test6: Group of three, with pairs straddling boundary.
    stellium_test_run([1,1,1,120,120,120,200,200,200,250,358,358,358])
    #Test6: Group of three, with one group over boundary.
    #Fails
    stellium_test_run([0,1,120,120,120,200,200,200,200,340,340,340,359])
    #Test7: One set of nine, the rest in another clump.
    stellium_test_run([100,100,100,100,100,100,100,100,100,200,200,200,200])
    #Test8: Group of nine, around the boundaries.
    stellium_test_run([1,1,1,1,1,1,1,1,1,358,358,358,358])
    #Test9: Group of nine, over the boundaries.
    #Fails
    stellium_test_run([0,0,1,1,1,250,250,250,250,358,359,359,359])
    #Test: One clump of 6, another of 7, near each other.
    stellium_test_run([100,100,100,100,100,100,110,110,110,110,110,110,110])
    #Test: One clump of 6, another of 7, near each other, straddling boundary.
    stellium_test_run([359,359,359,359,359,359,1,1,1,1,1,1,1])
    #Test: One clump of 6, another of 7, over boundary.
    #Fails
    stellium_test_run([358,359,359,0,0,1,7,7,7,7,7,7,7])
    #Test: Everything in one house
    stellium_test_run([150,150,150,150,150,150,150,150,150,150,150,150,150])
    #Test: Everything near the boundary
    stellium_test_run([1,1,1,1,1,1,1,1,1,1,1,1,1])
    #Test: Everything over the boundary
    #Fails
    stellium_test_run([357,357,358,358,359,359,0,0,0,1,1,1,2])

if __name__ == "__main__":
    #test_stelliums()
    #test_all_bg_images()
    stellium_test_battery()
