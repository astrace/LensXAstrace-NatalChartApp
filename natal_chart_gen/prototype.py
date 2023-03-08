from datetime import datetime, timezone
import math
import multiprocessing
import os
from io import BytesIO

from PIL import Image, ImageFont, ImageDraw
from lambda_multiprocessing import Pool
#from kerykeion import KrInstance
import pytz
import swisseph as swe

import constants
import image_params
import utils

swe.set_ephe_path('./assets/ephe')

class Planet:
    """
    A class representing a planet in the solar system.

    Attributes:
    - name: A string representing the name of the planet.
    - sign: A string representing the zodiac sign where the planet is located.
    - images: A dictionary containing the paths to the planet image and the zodiac sign image.
    - position: A tuple (x, y) representing the current position of the planet in the sky.
    - abs_pos: A float representing the absolute position of the planet in the sky, measured in degrees counterclockwise from 0 degree Aries on the ecliptic.
    - dpos: A float representing the change in position of the planet in the sky, measured in degrees.

    Methods:
    - __str__(): Returns a string representation of the planet object, including the planet name, zodiac sign, and absolute position.

    Note:
    - The `images` attribute is a dictionary containing two keys: 'planet' and 'sign', each corresponding to the path to the planet image and the zodiac sign image, respectively.
    - The `position` attribute is a tuple representing the current x and y coordinates of the planet's position in the sky.
    - The `abs_pos` attribute is a float representing the absolute position of the planet in the sky, measured in degrees counterclockwise from 0 degree Aries on the ecliptic.
    - The `dpos` attribute is a float representing the change in position of the planet in the sky, measured in degrees.
    """

    def __init__(self, name, position, abs_pos, sign):
        self.name = name
        self.sign = sign
        self.images = {
            "planet": "{}/planets/{}.png".format("assets/images", name),
            "sign": "{}/signs/{}.png".format("assets/images", sign)
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
    A class representing a natal chart object.
    
    Attributes:
    -----------
    required_objects : frozenset
        A set of all required planet names.
    objects : dict
        A dictionary containing planet names as keys and corresponding Planet objects as values.
    jd : float or None
        Julian day number representing the date and time of the natal chart. If None, it is assumed that the 
        chart is for the current date and time.
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
        -----------
        planets : list
            A list of Planet objects representing the planets in the natal chart.
        jd : float or None, optional (default=None)
            Julian day number representing the date and time of the natal chart. If None, it is assumed that the 
            chart is for the current date and time.
        
        Raises:
        -------
        Exception : if any planet/object is missing in the chart
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

def generate(dt, geo, local=False):
    # TODO: elaborate on format of input
    # datetime has timezone

    if local:
        # for local generation/testing
        load_image = lambda filename: Image.open("assets/images/" + filename)
    else:
        load_image = utils.load_image

    tz = pytz.timezone('UTC')
    dt = dt.astimezone(tz)
    # calculate Julian day
    # requires hour input as decimal with fraction
    hour = dt.hour + (dt.minute + dt.second / 60) / 60
    jd = swe.julday(dt.year, dt.month, dt.day, hour)

    # NOTE: ascendant is very important for orienting entire chart
    _, ascmc = swe.houses(jd, geo[0], geo[1], bytes('W', 'utf-8'))
    asc = constants.SIGNS[int(ascmc[0] // 30)]

    # create planet object/layer list
    planets = []
    for name, no_body in constants.PLANET_NAMES.items():
        abs_pos = swe.calc_ut(jd, no_body)[0][0]
        pos = abs_pos % 30
        sign = constants.SIGNS[int(abs_pos // 30)]
        p = Planet(name, pos, abs_pos, sign)
        planets.append(p)

    # add angles
    for abs_pos, name in [(ascmc[0], 'Asc'), (ascmc[1], 'Mc')]:
        pos = abs_pos % 30
        sign = constants.SIGNS[int(abs_pos // 30)]
        p = Planet(name, pos, abs_pos, sign)
        planets.append(p)

    chart = Natal_Chart(planets, jd)
    return _generate(chart, load_image)

def _generate(chart, load_image):
    
    asc = chart.objects['Asc'].sign
    # set background image
    bg_im = set_background(asc, load_image)
    
    # allows for writing text on image
    draw = ImageDraw.Draw(bg_im)
    font = ImageFont.truetype("assets/Inter-Medium.ttf", image_params.TEXT_SIZE)

    # custom rendering algos
    # NOTE: `spread_planets` might change the `dpos` attribute (side effect)
    utils.spread_planets(list(chart.objects.values()))

    for p in chart.objects.values():
        im = Image.open(p.images['planet'])#.convert('RGBa')
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
        im = Image.open(p.images['sign'])#.convert('RGBa')
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

#paste_fn(bg_im, obj, x, y)

def set_background(asc, load_image_fn=utils.load_image):
    # TODO: Parameterize filenames and put in `constants.py`
    bg_color = load_image_fn('background_color.png')
    bg_signs = load_image_fn('signs2.png')
    bg_houses = load_image_fn('house_numbers.png')
    logo = load_image_fn('astrace_logo.png')

    # rotate zodiac wheel so ascendant is in the first house
    bg_signs = bg_signs.rotate(-30 * constants.SIGNS.index(asc))
    # combine background color with zodiac wheel
    bg_im = Image.alpha_composite(bg_color, bg_signs)
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
    # get (x,y) location of 0 degree Aries

    """
    Calculates the position of a point that is `r` units away from a center point (`a`, `b`) at an angle of `theta` degrees from the point that is located `deg` degrees counterclockwise from 0 degree Aries on the ecliptic.

    Args:
    - asc: A string representing the zodiac sign where 0 degree Aries is located.
    - a: A float representing the x-coordinate of the center point.
    - b: A float representing the y-coordinate of the center point.
    - r: A float representing the distance from the center point to the point of interest.
    - theta: A float representing the angle between the line connecting the center point and the point of interest and the x-axis.

    Returns:
    A tuple (u, v) representing the position of the point of interest after being rotated around the center point (`a`, `b`) by an angle `theta` degrees counterclockwise.

    Note:
    - The `asc` argument should be a string representing a zodiac sign, where 0 degree Aries is located. It is used to calculate the starting position of the point on the ecliptic.
    - The function `rotate()` is used to calculate the resulting position after rotation around the center point.
    """

    deg = -90 - constants.SIGNS.index(asc) * 30
    x = a + r * math.sin(math.radians(deg))
    y = b + r * math.cos(math.radians(deg))
    # then rotate
    (u, v) = rotate(a, b, x, y, theta)
    return (u, v)

def rotate(a, b, s, t, deg):
    # -> circle with center (a,b)
    # return resulting position when rotating `deg`
    # degrees from starting position (s,t)

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
    #dt = tz.localize(datetime(1991, 4, 1, hour=17, minute=55))
    # stellium
    #dt = tz.localize(datetime(1962, 2, 4, hour=17, minute=55))
    #dt = tz.localize(datetime(1994, 1, 11, hour=3, minute=33))
    geo = (44.20169, 17.90397)

    """
    Tuesday, January 11 1994, 07:33 AM
    Sarajevo, Bosnia & Herzegovina
    """
    dt = tz.localize(datetime(1994, 1, 11, hour=7, minute=33))

    im = generate(dt, geo, local=True)
    im.show()

