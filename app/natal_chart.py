from datetime import datetime, timezone
from io import BytesIO
from numpy.random import choice
from pathlib import Path
import math
import multiprocessing
import re
import os

from PIL import Image, ImageFont, ImageDraw
import pytz
import swisseph as swe

from constants import EPHE_DIR, IMG_DIR, IMG_FILES, PLANET_NAMES, SIGNS
import image_params
import utils

swe.set_ephe_path(EPHE_DIR)

class Planet:
    """
    Attributes:
    - name: A string representing the name of the planet.
    - sign: A string representing the zodiac sign associated with the planet.
    - images: A dictionary containing the paths to the planet images and the zodiac sign images.
    - position: A float between 0 (inclusive) to 30 (exclusive) degrees, representing our angle on the plane.
    - abs_pos: A float representing the absolute angle in the plane, measured in degrees going counterclockwise.
    - dpos: Display Position - A float representing a (possible) change in abs_pos in the plane, measured in degrees.

    Methods:
    - __str__(): Returns a string representation of the planet object.

    Notes: 
        - By default, dpos = abs_pos on initialization. 
        - The spread_planets() function may change dpos to calculate an angle offset, for display purposes.
    """

    def __init__(self, name, position, abs_pos, sign):
        self.name = name
        self.sign = sign
        self.images = {
            "planet": IMG_FILES['PLANETS'][name.upper()],
            "sign": IMG_FILES['SIGNS'][sign.upper()]
        }
        self.position = position
        self.abs_pos = abs_pos
        self.dpos = abs_pos # subject to change
    def __str__(self):
        # for debugging
        return "{}; sign: {}, abs_pos: {:.2f}".format(
            self.name, self.sign, self.abs_pos
        )

class Natal_Chart:
    """
    Attributes:
        -required_objects: A frozenset of all required planet names.
        -objects: A dictionary containing planet names as keys and corresponding Planet objects as values.
        -jd : Julian day integer representing the date and time of the natal chart. If None, it is assumed that the 
        chart is for the current date and time.

    Notes:
        - The Julian date format is used becasue the swisseph astrolibrary requires it.
    """
    required_objects = frozenset([
        "Sun", "Moon", "Venus", "Mars",
        "Jupiter", "Saturn", "Uranus", "Neptune",
        "Pluto", "North Node", "Chiron",
        "Asc", "Mc"
    ])

    def __init__(self, planets, jd=None):
        """
        Parameters:
        - planets: A list of Planet objects representing the planets in the natal chart.
        - jd : optional (default=None) Julian day number representing the date and time of the natal chart. If None, it is assumed that the 
            chart is for the current date and time.
        
        Raises:
        - Exception : if any planet/object is missing in the chart
        """
        self.objects = {}
        for p in planets:
            self.objects[p.name] = p
        s1 = set(self.objects.keys())
        if s1 != self.required_objects:
            raise Exception(
                'Planets/Objects missing:',
                self.required_objects - s1 
            )
        self.jd = jd


def generate(local_time: str, location: str, local: bool = False) -> Image:
    """
    Generate a natal chart based on birth information.

    Args:
        local_time (str):
            Local date and time of birth in ISO 8601 format (YYYY-MM-DDTHH:MM:SS).
        location (str):
            Geographical coordinates of birth location in the format 'LAT,LON',
            where LAT is the latitude and LON is the longitude.
        local (bool, optional):
            Generate natal chart locally. This is useful for visual testing.
            Note: When running locally, the program will read image files from the local file system
            instead of fetching them from S3. (default: False)

    Returns:
        Image: A PIL Image object representing the generated natal chart.

    Raises:
        ValueError: If the input arguments are invalid.

    Example usage:
        generate('2022-01-01T12:00:00', '40.7128,-74.0060')
    """

    # Check that local_time is a valid ISO 8601 date and time
    try:
        dt = datetime.fromisoformat(local_time)
    except ValueError:
        raise ValueError(
            f"Invalid local_time: {local_time}."
            " Must be in ISO 8601 format (YYYY-MM-DDTHH:MM:SS)."
        )
    # Check that location is a valid latitude and longitude string
    try:
        lat, lon = location.split(',')
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        raise ValueError(
            f"Invalid location: {location}."
            " Must be in the format 'LAT,LON',"
            " where LAT is the latitude and LON is the longitude."
        )
    # Check that local is a boolean
    if not isinstance(local, bool):
        raise ValueError(
            f"Invalid local parameter: {local}. "
            " Must be a boolean value."
        )

    if local:
        # for local generation/testing
        image_loader = utils.LocalImageLoader(IMG_DIR)
    else:
        # read from environment vars passed during deployment
        image_loader = utils.RemoteImageLoader(
            os.environ['CLOUDFRONT_DISTRIBUTION_URL'],
            os.environ['IMG_LAYER_BUCKET_NAME'],
        )

    # calculate Julian day
    # requires hour input as decimal with fraction
    hour = dt.hour + (dt.minute + dt.second / 60) / 60
    jd = swe.julday(dt.year, dt.month, dt.day, hour)
    _, ascmc = swe.houses(jd, lat, lon, bytes('W', 'utf-8'))

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

    chart = Natal_Chart(planets, jd)
    return _generate(chart, image_loader)

def _generate(chart, image_loader, bg_file=None):
    """
     This is a hidden/helper function for the main generate() function.

     The actual building of the image (piecing together background placement, rotation, and object-sign pairs...)
     is done here. The clumps algorithm is also run from here.

     Returns a constructed image, built with the PIL library.
    
    """
    if not bg_file:
        bg_file = random_asset(IMG_FILES['BACKGROUNDS'])

    asc = chart.objects['Asc'].sign
    # set background image
    bg_im = set_background_layers(asc, bg_file, image_loader)
    
    # allows for writing text on image
    draw = ImageDraw.Draw(bg_im)
    font = ImageFont.truetype("fonts/Inter-Medium.ttf", image_params.TEXT_SIZE)

    # NOTE: `spread_planets` might change the `dpos` attribute (side effect)
    utils.spread_planets(list(chart.objects.values()))

    for p in chart.objects.values():
        """
        Each planet-text-sign image grouping is constructed here.
        """
        im = image_loader.load(p.images['planet'])
        # add planet
        add_object(
            im,
            bg_im,
            p.dpos,
            asc,
            image_params.PLANET_SIZE,
            image_params.PLANET_RADIUS,
            lambda bg_im, obj, x, y: bg_im.paste(obj, (x,y), obj)
        )
        im = image_loader.load(p.images['sign'])
        # add sign
        add_object(
            im,
            bg_im,
            p.dpos,
            asc,
            image_params.SIGN_SIZE,
            image_params.SIGN_RADIUS,
            lambda bg_im, obj, x, y: bg_im.paste(obj, (x,y), obj)
        )
        # add text
        # see: https://stackoverflow.com/questions/1528932/how-to-create-inline-objects-with-properties
        add_object(
            type('obj', (object,), {'size' : (image_params.TEXT_SIZE, image_params.TEXT_SIZE)}), # update sizing
            bg_im,
            p.dpos,
            asc,
            None,
            image_params.TEXT_RADIUS,
            lambda bg_im, obj, x, y: draw.text((x,y), "{}°".format(math.floor(p.position)), font=font),
            False
        )
    return bg_im


def random_asset(asset_dict):
    """
        A helper function that selects a random asset filename, given a probability dictionary. Just wraps numpy.random.choice()

        Args:
            - asset_dict: A dictionary that has asset filenames for keys, mapping to probability values

        Returns:
            - asset_name: A string name that was chosen from the dictionary.

        Exceptions:
            - ValueError: thrown by numpy if probabilities of dictionary are not normalized.
            
        Notes:
            - This wrapper is pretty shallow - it just hides the more long-winded code seen in the return statement below.
            - If the randomness functionality does not expand in the future, this function wrapper should be removed.
    """
    return choice(list(asset_dict.keys()), p=list(asset_dict.values()))


def set_background_layers(asc, bg_file, image_loader):
    """
    Creates a composite image consisting of a Zodiac Sign, House and Logo Layer overlayed together.

    Args:
        asc (str): The ascendant sign, one of the 12 zodiac signs.
        bg_file (str): The filename of the background image

    Returns:
        Image: A composite image containing the background color, the zodiac wheel rotated so that the ascendant is in the first house,
               the house numbers, and the logo.

    Raises:
        FileNotFoundError: If any of the required image files cannot be found in the current directory.
    """
    # TODO: Parameterize filenames and put in `constants.py`
    bg = image_loader.load(bg_file)
    bg_signs = image_loader.load(IMG_FILES['ZODIAC_WHEEL'])
    bg_houses = image_loader.load(IMG_FILES['HOUSE_NUMBERS'])
    logo = image_loader.load(IMG_FILES['LOGO'])

    # rotate zodiac wheel so ascendant is in the first house
    bg_signs = bg_signs.rotate(-30 * SIGNS.index(asc))
    # combine background color with zodiac wheel
    bg_im = Image.alpha_composite(bg, bg_signs)
    # remove alpha channel (makes pasting layers simpler)
    bg_im = bg_im.convert("RGB")
    # paste house numbers
    bg_houses = resize_image(bg_houses, bg_im.size, image_params.HOUSE_NUMBER_RADIUS)
    (a, b) = get_center(bg_im.size, bg_houses.size)
    bg_im.paste(bg_houses, (a,b), bg_houses)
    # paste logo
    logo = resize_image(logo, bg_im.size, image_params.LOGO_RADIUS)
    (a, b) = get_center(bg_im.size, logo.size)
    bg_im.paste(logo, (a,b), logo)
    return bg_im

def get_center(bg_size, fg_size):
    """
    Returns the offset necessary to center an image with size `fg_size` on a background image with size `bg_size`.

    Args:
    - bg_size: A tuple (width, height) representing the size of the background image.
    - fg_size: A tuple (width, height) representing the size of the image to be centered.

    Returns:
    A tuple (offset_w, offset_h) representing the offset necessary to center the image on the background image.
    """
    bg_w, bg_h = bg_size
    img_w, img_h = fg_size
    offset_w = (bg_w - img_w) // 2
    offset_h = (bg_h - img_h) // 2
    return offset_w, offset_h

def resize_image(im, bg_size, p):
    """
    Resizes the input image `im` to a new size that is `p` percent of the `bg_size` image size.

    Args:
    - im: The input image to be resized.
    - bg_size: A tuple (width, height) representing the size of the background image.
    - p: A float representing the percentage of the `bg_size` image size to which the `im` should be resized.

    Returns:
    The resized image as a PIL Image object.
    """
    new_width = p * bg_size[0]
    new_height = (new_width / im.size[0]) * im.size[1]
    new_size = tuple(map(int, (new_width, new_height)))
    return im.resize(new_size, Image.LANCZOS)

def get_coordinates(asc, a, b, r, theta):
    """
    Calculates the position of a point that is `r` units away from a center point (`a`, `b`) at an angle of `theta` degrees from the point that is located `deg` degrees counterclockwise from 0 degree Aries on the ecliptic.

    Args:
    - asc: A string representing the zodiac sign.
    - a: A float representing the x-coordinate of the center point.
    - b: A float representing the y-coordinate of the center point.
    - r: A float representing the distance from the center point to the point of interest.
    - theta: A float representing the angle from line connecting the center point (a,b), and calculated point (x,y). Used to 
    rotate (x,y) about (a,b), yielding the point (u,v).

    Returns:
    A tuple (u, v) representing the position of the point of interest after being rotated around the center point (`a`, `b`) by an angle `theta` degrees counterclockwise.

    Note:
    - The `asc` argument should be a string representing a zodiac sign.
    - The function `rotate()` is used to calculate the resulting position after rotation around the center point.
    """
    # get (x,y) location of 0 degree Aries
    deg = -90 - SIGNS.index(asc) * 30
    x = a + r * math.sin(math.radians(deg))
    y = b + r * math.cos(math.radians(deg))
    # then rotate
    (u, v) = rotate(a, b, x, y, theta)
    return (u, v)

def rotate(a, b, s, t, deg):
    """
    Rotates the point (`s`, `t`) around the point (`a`, `b`) by `deg` degrees and returns the resulting position.

    Args:
    - a: A float representing the x-coordinate of the center of the circle.
    - b: A float representing the y-coordinate of the center of the circle.
    - s: A float representing the x-coordinate of the point to be rotated.
    - t: A float representing the y-coordinate of the point to be rotated.
    - deg: A float representing the angle by which the point (`s`, `t`) should be rotated in degrees.

    Returns:
    A tuple (u, v) representing the resulting position of the rotated point.
    """
    # -> circle with center (a,b)
    # return resulting position when rotating `deg`
    # degrees from starting position (s,t)
    cos_theta = math.cos(math.radians(deg))
    sin_theta = math.sin(math.radians(deg))
    u = a + (s - a) * cos_theta + (t - b) * sin_theta
    v = b - (s - a) * sin_theta + (t - b) * cos_theta
    return (u, v)
    
def add_object(
        obj,
        bg_im,
        dpos,
        asc,
        obj_size,
        obj_radius,
        paste_fn,
        resize=True
    ):
    if resize:
        # resize obj image
        obj = resize_image(obj, bg_im.size, obj_size)
    # get center of circle
    # distance from center as % of background image
    r = obj_radius * bg_im.size[1]
    # TODO: change name to "get center"?
    (a, b) = get_center(bg_im.size, obj.size)
    # b += 5 # TODO: formalize vertical offset so 0 is exactly on horizontal
    # OR: edit image so that 
    (x, y) = get_coordinates(asc, a, b, r, dpos)
    x = round(x)
    y = round(y)

    paste_fn(bg_im, obj, x, y)
    return bg_im


if __name__ == "__main__":
    tz = pytz.timezone('Europe/London')
    #tz = pytz.timezone('America/New_York')
    
    
    #dt = tz.localize(datetime(1991, 4, 1, hour=17, minute=55))
    # stellium
    #dt = tz.localize(datetime(1962, 2, 4, hour=17, minute=55))
    #dt = tz.localize(datetime(1994, 1, 11, hour=3, minute=33))
    geo = (44.20169, 17.90397)
    #geo = (45.4215, 75.6972)
    """
    Tuesday, January 11 1994, 07:33 AM
    Sarajevo, Bosnia & Herzegovina
    """
    dt = tz.localize(datetime(1994, 1, 11, hour=7, minute=33))
    #dt = tz.localize(datetime(1987,11,8,hour=0,minute=5))
    
    # To generate a natal chart, we need a date of birth + time of day (with time-zone), and location on Earth.
    im = generate(dt, geo, local=True)
    im.show()

