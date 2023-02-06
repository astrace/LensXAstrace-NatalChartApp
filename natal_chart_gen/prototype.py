import datetime
import math
import multiprocessing
import numpy as np
import os
from io import BytesIO

from PIL import Image, ImageFont, ImageDraw
from lambda_multiprocessing import Pool
from kerykeion import KrInstance

import constants
import image_params
import utils

class Planet:
    def __init__(self, name, position, abs_pos):
        self.name = name
        self.image_fname = '{}/{}.png'.format("images", name)
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
        load_image = lambda filename: Image.open("images/" + filename)
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
        p = Planet(name, pos, abs_pos)
        planets.append(p)
  
    # TODO: come up with more principled way to do this (i.e. not just running it twice)
    # NOTE: `spread_planets` might change the `display_pos` attribute
    spread_planets(planets)
    spread_planets(planets)
    
    for p in planets:
        im = Image.open(p.image_fname)#.convert('RGBa')
        add_planet(im, bg_im, p.position, p.display_pos, asc)

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
    
def add_planet(im, bg_im, position, display_pos, asc):
    # resize planet image
    im = resize_image(im, bg_im.size, image_params.PLANET_SIZE)
    # get center of circle
    # distance from center as % of background image
    r = image_params.PLANET_RADIUS * bg_im.size[1]
    # TODO: change name to "get center"?
    (a, b) = get_center(bg_im.size, im.size)
    b += 5 # TODO: formalize vertical offset so 0 is exactly on horizontal
    (x, y) = get_coordinates(asc, a, b, r, display_pos)
    x = round(x)
    y = round(y)
    bg_im.paste(im, (x,y), im)
    
    # add text
    draw = ImageDraw.Draw(bg_im)
    font = ImageFont.truetype("Inter-Medium.ttf", 34)
    draw.text((x,y), "{:.0f}".format(position), font=font)

    return bg_im

def find_clumps(planets, theta):
    # TODO: explain what `theta` is
    # returns list of lists
    # - sort planets according to location on perimeter
    planets.sort(key=lambda p: p.abs_pos)
    # find "clumps"
    clumps = []
    curr_clump = []
    
    def _clump_check(p_1, p_n, n):
        return abs(p_n - p_1) < theta * (n - 1)
    
    i = 0
    while i < len(planets):
        p = planets[i]
        
        # if it's the first planet, add it to current (empty) clump
        # ow (or) check if the current planet belongs to the current clump
        if i == 0 or _clump_check(curr_clump[0].abs_pos, p.abs_pos, 1 + len(curr_clump)):
            curr_clump.append(p)
            
        else:
            clumps.append(curr_clump)
            curr_clump = [p]
        
        i += 1
        
    clumps.append(curr_clump)
    
    # final check to see if there's a clump near 0 / 360
    first_planet_pos = clumps[0][0].abs_pos
    last_planet_pos = clumps[-1][-1].abs_pos
    n = len(clumps[0]) + len(clumps[-1])
    if _clump_check(first_planet_pos, last_planet_pos, n):
        # merge
        # TODO: Test this !!!
        clumps[0] = clumps[-1] + clumps[0]
        clumps = clumps[:-1]
        
    return clumps

def spread_planets(planets, min_dist=0):
    # `min_dist` is degrees apart that planets should be displayed
    # in addition to width apart
    # reason: stelliums etc.
    # note: planet objects are changed within this function
    # TODO: consider way to doing this without side effects
    
    # first: find a clump
    # "clump" definition: x planets in a sector not having a total acceptable min width
    
    # convert planet size to approximate degrees it takes up
    # treats planet width as chord length & planet radius as radius; solve for angle
    theta = math.degrees(2 * math.asin(0.5 * (image_params.PLANET_SIZE / 2) / image_params.PLANET_RADIUS)) 
    
    clumps = find_clumps(planets, theta)
    
    for clump in clumps:
        n = len(clump)
        if n == 1:
            continue
        # spread across min distance
        min_distance = len(clump) * theta
        center_point = (clump[0].abs_pos + clump[-1].abs_pos) / 2
        new_positions = np.arange(
            center_point - (n / 2) * theta,
            center_point + (n / 2) * theta,
            theta
        )
        # set display positions
        for (p, pos) in zip(clump, new_positions):
            p.display_pos = pos


if __name__ == "__main__":
    dt = datetime.datetime(1991, 4, 1)
    im = generate("zenica", dt, local=True)
    im.show()
