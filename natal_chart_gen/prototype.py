import datetime
import math
import multiprocessing
import os
from io import BytesIO

from PIL import Image, ImageFont, ImageDraw
from lambda_multiprocessing import Pool
from kerykeion import KrInstance

import constants
import image_params
import utils

class Planet:
    def __init__(self, name, position, abs_pos, sign):
        self.name = name
        self.images = {
            "planet": "{}/planets/{}.png".format("assets/images", name),
            "sign": "{}/signs/{}.png".format("assets/images", sign)
        } 
        self.position = position
        self.abs_pos = abs_pos
        self.display_pos = abs_pos # subject to change
    def __str__(self):
        # for debugging
        return "{}; abs_pos: {:.2f}".format(self.name, self.abs_pos)

def generate(location_string, dt, local=False):
    # TODO: elaborate on format of input

    if local:
        # for local generation/testing
        load_image = lambda filename: Image.open("assets/images/" + filename)
    else:
        load_image = utils.load_image

    chart = KrInstance("", dt.year, dt.month, dt.day, dt.hour, dt.minute, location_string)
    # NOTE: ascendant is very important for orienting entire chart
    asc = chart.first_house["sign"]

    # set background image
    bg_im = set_background(asc, load_image)
    
    # create planet object/layer list
    planets = []
    for name in constants.PLANET_NAMES:
        pos = chart.__dict__[name.lower()].position
        abs_pos = chart.__dict__[name.lower()].abs_pos
        sign = chart.__dict__[name.lower()].sign
        p = Planet(name, pos, abs_pos, sign)
        planets.append(p)
  
    # TODO: come up with more principled way to do this (i.e. not just running it twice)
    # NOTE: `spread_planets` might change the `display_pos` attribute
    utils.spread_planets(planets)
    utils.spread_planets(planets)
    
    for p in planets:
        im = Image.open(p.images['planet'])#.convert('RGBa')
        add_object(
            im,
            bg_im,
            p.display_pos,
            asc,
            image_params.PLANET_SIZE,
            image_params.PLANET_RADIUS,
            lambda bg_im, obj, x, y: bg_im.paste(obj, (x,y), obj)
        )
    return bg_im

def set_background(asc, load_image_fn=utils.load_image):
    # TODO: Parameterize filenames and put in `constants.py`
    bg_color = load_image_fn('background_color.png')
    bg_signs = load_image_fn('signs.png')
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
    # TODO: description; needed in order to center image
    bg_w, bg_h = bg_size
    img_w, img_h = fg_size
    offset_w = (bg_w - img_w) // 2
    offset_h = (bg_h - img_h) // 2
    return offset_w, offset_h

def resize_image(im, bg_size, p):
    # resize planet as `p` percent of blackground image
    new_width = p * bg_size[0]
    new_height = (new_width / im.size[0]) * im.size[1]
    new_size = tuple(map(int, (new_width, new_height)))
    return im.resize(new_size, Image.LANCZOS)

def get_coordinates(asc, a, b, r, theta):
    # get (x,y) location of 0 degree Aries
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
    cos_theta = math.cos(math.radians(deg))
    sin_theta = math.sin(math.radians(deg))
    u = a + (s - a) * cos_theta + (t - b) * sin_theta
    v = b - (s - a) * sin_theta + (t - b) * cos_theta
    return (u, v)
    
def add_object(
        obj,
        bg_im,
        display_pos,
        asc,
        obj_size,
        obj_radius,
        paste_fn
    ):
    # resize planet image
    obj = resize_image(obj, bg_im.size, obj_size)
    # get center of circle
    # distance from center as % of background image
    r = obj_radius * bg_im.size[1]
    # TODO: change name to "get center"?
    (a, b) = get_center(bg_im.size, obj.size)
    # b += 5 # TODO: formalize vertical offset so 0 is exactly on horizontal
    # OR: edit image so that 
    (x, y) = get_coordinates(asc, a, b, r, display_pos)
    x = round(x)
    y = round(y)

    paste_fn(bg_im, obj, x, y)
    return bg_im


if __name__ == "__main__":
    dt = datetime.datetime(1991, 4, 1, 17, 55)
    im = generate("zenica", dt, local=True)
    im.show()
