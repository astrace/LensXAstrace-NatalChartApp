import bisect
import math
import numpy as np
import os
import requests
import tempfile
from io import BytesIO
from pathlib import Path

import boto3
from PIL import Image
from copy import deepcopy

import image_params

class ImageLoader:
    def load(self, file_path: str) -> Image:
        pass

class LocalImageLoader(ImageLoader):
    def __init__(self, image_dir):
        self.image_dir = image_dir
        self.image_cache = {}

    def load_all_images(self):
        def _load_all_images(fname):
            if os.path.isdir(fname):
                for fname2 in os.listdir(self.image_dir):
                    _load_all_images(fname2)
            else:
                if fname[-4:] not in ['.png', 'jpg']:
                    return
                file_path = Path(self.image_dir) / fname
                self.image_cache[fname] = Image.open(file_path)
        _load_all_images(self.image_dir)

    def load(self, filename: str) -> Image:
        if filename not in self.image_cache:
            file_path = Path(self.image_dir) / filename
            self.image_cache[filename] = Image.open(file_path)
        return self.image_cache[filename]

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
        This helper function takes the angular positions of two planets
        and the number of planets between them and determines whether
        the two planets are considered part of the same clump. The
        maximum angular distance that two planets can be apart and still be
        considered part of the same clump is determined by the value of "theta".
        """
        return abs(pn - p1) < theta * (n - 1)
   
    def _pass(planets):
        clumps = []
        curr_clump = []
        
        for i,p in enumerate(planets):
            if i == 0:
                # if it's the first planet, add it to current (empty) clump
                curr_clump.append(p)
                continue

            # get current clump info
            p1 = curr_clump[0].dpos
            p2 = p.dpos # potentially not part of current clump
            n = 1 + len(curr_clump)
            
            if _clump_check(p1, p2, n):
                # if it satisfies the clump criteria, add it to the current clump
                curr_clump.append(p)
            else:
                clumps.append(curr_clump)
                curr_clump = [p]

        clumps.append(curr_clump)
        return clumps

    # hard to explain why this needs to be done twice: forward & backwards pass
    # ... there are edge cases where one pass fails
    planets.sort(key=lambda p: p.dpos)
    # NOTE: We add first planet again to the end in case of clumps near 0/360
    ##Note2: We must make a deep copy - because the dpos will change for both the p0 at the beginning and ends.
    """ Old code (with shallow copying)
    p0 = planets[0]
    p0.dpos += 360
    clumps1 = _pass(planets + [p0])
    """
    pEnd = deepcopy(planets[0])
    pEnd.dpos += 360
    clumps1 = _pass(planets + [pEnd])
    

    planets.sort(key=lambda p: p.dpos, reverse=True)
    clumps2 = _pass(planets)

    """
    //Used for debugging - will remove when pull request finished.
    print("We ran two passes, and found two sets of clumps. Heres what we got:")
    print("Clumps1 List:")
    for clump in clumps1:
        print(str([str(p) for p in clump]))

    print("Clumps2 List:")
    for clump in clumps2:
        print(str([str(p) for p in clump]))
    """

    # TODO: CHECK FOR CLUMPS NEAR 0/360

    clumps = _merge_clumps(clumps1, clumps2)
    clumps = _split_clumps_by_sign(clumps) 
    # remove singletons
    clumps = [c for c in clumps if len(c) > 1]
    
    return clumps

def _merge_clumps(clumps1, clumps2):
    """"(
    Merges two lists of integer clusters into a single list of merged clusters.

    Args:
        clumps1 (List[List[int]]): A list of integer clusters, represented as lists of integers.
        clumps2 (List[List[int]]): A second list of integer clusters, also represented as lists of integers.

    Returns:
        A list of merged integer clusters, where each cluster is represented as a list of integers.

    """
    clumps1 = [c for c in clumps1 if len(c) > 1]
    clumps2 = [c for c in clumps2 if len(c) > 1]
    clumps = set() # merged
    for c1 in clumps1:
        for c2 in clumps2:
            c1, c2 = set(c1), set(c2)
            if c1 == c2:
                clumps.add(frozenset(c1))
            elif len(c1 & c2) > 0:
                clumps.add(frozenset(c1 | c2))
    """ Used for debugging - remove once pull request finished.
    print("Our merged clump list:")
    for clump in clumps:
        print(str([str(p) for p in clump]))
    """
    return [list(c) for c in clumps]


def _split_clumps_by_sign(clumps):
    # this is needed for proper rendering in `spread_planets`
    """
    Splits a list of planet clusters by sign, and returns a new list of clusters.

    Args:
        clumps (List[List[Planet]]): A list of planet clusters, represented as lists of `Planet` objects.

    Returns:
        A list of planet clusters, where each cluster is sorted by degree and split into multiple clusters by sign.

    Note:
        This function is specifically designed for use in the `spread_planets` function.
    """
    new_clumps = []
    for c in clumps:
        c.sort(key=lambda p: p.dpos)
        if c[0].sign != c[-1].sign:
            i = 0
            while c[i].sign != c[-1].sign:
                i += 1
            new_clumps.append(c[:i])
            new_clumps.append(c[i:])
        else:
            new_clumps.append(c)
    """ Used for debugging.
    print("Regrouping clumps by sign. Output below:")
    for clump in new_clumps:
        print(str([str(p) for p in clump]))
    """
    return new_clumps
        

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
    
        assert len(clump) > 1

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

