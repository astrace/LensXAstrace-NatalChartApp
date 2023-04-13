import bisect
import math
import numpy as np
import os
import requests
import tempfile
from io import BytesIO
from pathlib import Path

import boto3
from disjoint_set import DisjointSet
from PIL import Image
from copy import deepcopy

import image_params

class ImageLoader:
    def load(self, file_path: str) -> Image:
        pass

class LocalImageLoader(ImageLoader):
    def __init__(self, image_dir, image_files):
        self.image_dir = image_dir
        self.image_files = image_files
        self.image_cache = {}
        # not exactly optimal to load background image twice,
        # but also not *that* inefficient
        self.bg_im_size = self.load(list(image_files['BACKGROUNDS'].keys())[0]).size[0]

    def load_all_images(self):
        def _load_all_images(d: dict):
            for k,v in d.items():
                if type(v) == str:
                    self.load(v)
                elif type(v) in [int, float]:
                    self.load(k)
                else:
                    _load_all_images(v)

        _load_all_images(self.image_files)

    def load(self, filename: str) -> Image:
        if filename not in self.image_cache:
            print(f'Loading {filename}')
            file_path = Path(self.image_dir) / filename
            self.image_cache[filename] = Image.open(file_path)
        return self.image_cache[filename]

    def resize_all_images(self):
        for (fname, p) in [
            # zodiac wheel
            (self.image_files['HOUSE_NUMBERS'], image_params.HOUSE_NUMBER_RADIUS),
            # logo
            (self.image_files['LOGO'], image_params.LOGO_RADIUS),
            # planets
            *[(sign, image_params.PLANET_SIZE) for sign in self.image_files['PLANETS'].values()],
            # signs 
            *[(sign, image_params.SIGN_SIZE) for sign in self.image_files['SIGNS'].values()],
        ]:
            im  = self.load(fname)
            print(f"Resizing {fname} to {100*p}% of background.")
            self.image_cache[fname] = resize_image(im, self.bg_im_size, p)
        

class RemoteImageLoader:
    def __init__(self, distribution_url, bucket_name):
        self.distribution_url = distribution_url
        self.bucket_name = bucket_name
        self.s3 = boto3.client('s3')
        # load all files to temporary directory
        self.tmp_dir = tempfile.TemporaryDirectory()
    
    def load(self, image_key):
        url = f"https://{self.distribution_url}/{image_key}"
        response = requests.get(url)
        file_path = Path(self.tmp_dir.name) / image_key\
        # create directories if they don't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        return Image.open(file_path)

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
    new_width = p * bg_size
    new_height = (new_width / im.size[0]) * im.size[1]
    new_size = tuple(map(int, (new_width, new_height)))
    return im.resize(new_size, Image.LANCZOS)

def calculate_position(degree):
    return {
        "sign": constants.SIGNS.index(degree // 30),
        "position": degree % 30
    }

def find_clumps(planets, theta):
    """Find clumps of planets located near each other on the perimeter of a circle.

    Args:
        planets (list): A list of Planet objects.
        theta (float):  A float value indicating the maximum angular distance
                        that two planets can be apart and still be considered
                        part of the same clump.

    Returns:
        list: A list of lists, where each inner list contains the planets that are part
              of the same clump.

    This function sorts the planets based on their location on the perimeter of a circle
    and then iterates through the sorted list to find clumps of planets that are close
    to each other. It does this by performing two passes through the list of planets: one
    forward pass and one backward pass. It then merges the clumps found in each pass and
    returns a list of unique clumps. If two clumps overlap, they are merged into a single
    clump.
    """
    def _clump_check(p1, pn, n):
        """
        This helper function takes two planets
        and the number of planets between them and determines whether
        the two planets are considered part of the same clump. The
        maximum angular distance that two planets can be apart and still be
        considered part of the same clump is determined by the value of "theta".
        """
        return (p1.sign == pn.sign) and abs(p1.dpos - pn.dpos) < theta * (n - 1)
  
    # using Disjoint-set data structure for keeping track of clumps
    # https://en.wikipedia.org/wiki/Disjoint-set_data_structure

    clumps = DisjointSet()

    def _pass(planets):
        curr_first_planet = planets[0]
        curr_size = 1 

        for p in planets[1:]:
            # ensure each planet has it's own set
            # NOTE: `find` creates a size-1 set if
            # the element is currently not in the ds
            clumps.find(p)

            if _clump_check(curr_first_planet, p, curr_size + 1):
                # if it satisfies the clump criteria, add it to the current clump
                clumps.union(curr_first_planet, p)
                curr_size += 1
            else:
                curr_first_planet = p
                curr_size = 1

    # forward and backwards pass
    _pass(sorted(planets, key=lambda p: p.dpos))
    _pass(sorted(planets, key=lambda p: p.dpos, reverse=True))

    # sort planets in clumps before returning
    ret = list(sorted(list(c), key=lambda x: x.dpos) for c in clumps.itersets())
    return ret

def spread_planets(planets, theta=None, min_to_center=5):
    """
    Spread planets across the perimeter of a circle
    with a minimum angular separation of theta
    between two neighboring planets.

    Args:
        planets (list):
            A list of Planet objects.
        theta (float, optional):
            A float value indicating the minimum angular separation between
            adjacent planets on the perimeter of a circle. If not specified, 
            the value is calculated based on the size and radius of the 
            planet images.
        min_to_center (int, optional):
            An integer value indicating the minimum number of planets
            required to center the group at the midpoint of a house.
            If there are fewer than this number of planets
            in the group, the center point will be the midpoint of the 
            group's angular range.

    Returns:
        None. Modifies the display positions of the planets in place.

    This function first finds clumps of planets located near
    each other on the perimeter of a circle, using the `find_clumps`
    function. For each clump, it calculates a new position for each
    planet in the clump based on the desired angular separation and
    the number of planets in the clump.

    Note:
        This function modifies the display positions
        of the planets in place. 
    """

    if not theta:
        # convert planet size to approximate degrees it takes up
        # treats planet width as chord length & planet radius as radius; solve for angle
        theta = math.degrees(2 * math.asin(0.5 * (image_params.PLANET_SIZE / 2) / image_params.PLANET_RADIUS)) 

    clumps = find_clumps(planets, theta)

    for clump in clumps:
    
        if len(clump) <= 1:
            continue

        clump.sort(key=lambda p: p.dpos)
        n = len(clump)

        # spread across min distance
        min_distance = len(clump) * theta
        #center_point = _get_center_pt(clump, min_distance)

        if min_distance >= 30: # probably should do less
            # stellium takes up entire sign/house
            # put center of clump at center of sign/house
            house_cusp = clump[0].dpos - clump[0].dpos % 30
            center_point = house_cusp + 15
            center_point += theta / 2 # improve centering a bit
        else:
            center_point = (clump[0].dpos + clump[-1].dpos) / 2
            
            # check if this causes "bleeding" into *previous* house
            before = clump[0].dpos
            after = center_point - (n / 2) * theta
            
            # different sign?
            if before // 30 != after // 30:
                bleed_over = 30 - after % 30
                center_point += bleed_over
                center_point += theta / 2 # improve positioning

            # check if this causes "bleeding" into *next* house
            #S: Why is this done all over again?
            before = clump[-1].dpos
            after = center_point + (n / 2) * theta
            # different sign?
            if before // 30 != after // 30:
                bleed_over = after % 30
                center_point -= bleed_over
                center_point -= theta / 2 # improve positioning
        
        #S: Once all the centering and detection is done, we assign new positions
        new_positions = np.arange(
            center_point - (n / 2) * theta,
            center_point + (n / 2) * theta,
            theta
        )
        # set display positions
        for (p, pos) in zip(clump, new_positions):
            p.dpos = pos

def print_clumps(clumps):
    # just a helper for debugging
    for c in clumps:
        print([str(p) for p in c])

