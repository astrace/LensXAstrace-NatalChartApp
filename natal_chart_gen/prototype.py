import math
import multiprocessing
import os
from io import BytesIO

from PIL import Image
from lambda_multiprocessing import Pool
from kerykeion import KrInstance

import constants
import utils

SIGNS = ['Ari', 'Tau', 'Gem', 'Can', 'Leo', 'Vir', 'Lib', 'Sco', 'Sag', 'Cap', 'Aqu', 'Pis']

def generate(location_string, dt):
    # TODO: elaborate on format of input 

    bg_im = utils.load_image(constants.BACKGROUND_FILE)

    chart = KrInstance("", dt.year, dt.month, dt.day, dt.hour, dt.minute, location_string)

    asc = chart.first_house["sign"]

    # rotate background
    bg_im = rotate_background_based_on_ascendant(bg_im, asc)

    planet_ims = load_planet_images(constants.PLANET_FILES)

    planet_objs = [
        chart.sun,
        chart.mercury,
        chart.venus,
        chart.mars,
        chart.jupiter,
        chart.saturn,
        chart.uranus,
        chart.neptune,
        chart.pluto
    ]

    for (abs_pos, im) in zip([o['abs_pos'] for o in planet_objs], planet_ims):
        add_planet(im, bg_im, abs_pos, asc)

    return bg_im
    
def load_planet_images(fnames):
    result = []
    for fname in fnames:
        print("Loading {} ...".format(fname))
        im = utils.load_image(fname)
        result.append(im)
    return result

def rotate_background_based_on_ascendant(bg_im, asc):
    return bg_im.rotate(-30 * SIGNS.index(asc), fillcolor='black')
    
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
    deg = -90 - SIGNS.index(asc) * 30
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
    
def add_planet(im, bg_im, abs_pos, asc):
    # resize planet image
    im = resize_image(im, bg_im.size, 0.1)
    # get center of circle
    # distance from center as % of background image
    r = 0.25 * bg_im.size[1]
    (a, b) = get_center(bg_im.size, im.size)
    b += 5 # TODO: formalize vertical offset so 0 is exactly on horizontal
    (x, y) = get_coordinates(asc, a, b, r, abs_pos)
    x = round(x)
    y = round(y)
    bg_im.paste(im, (x,y), im)
    return bg_im

