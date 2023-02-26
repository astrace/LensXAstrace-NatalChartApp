import bisect
import math
import numpy as np
import requests
from io import BytesIO

import boto3
from PIL import Image

import constants
import image_params

def load_image(filename):
    url = constants.IMAGES_URL + filename
    print("Loading {} ...".format(url))
    resp = requests.get(url)
    im = Image.open(BytesIO(resp.content))
    return im

def read_image_from_s3(bucket, key, region_name='us-east-1'):
    print('Reading {} from S3 bucket {} ...'.format(key, bucket))
    s3 = boto3.client('s3')
    file_byte_string = s3.get_object(Bucket=bucket, Key=key)['Body'].read()
    x = BytesIO(file_byte_string)
    return Image.open(BytesIO(file_byte_string))
    
def write_image_to_s3(im, bucket, key, region_name='us-east-1'):
    s3 = boto3.resource('s3', region_name)
    bucket = s3.Bucket(bucket)
    object = bucket.Object(key)
    file_stream = BytesIO()
    im.save(file_stream, format='png')
    object.put(Body=file_stream.getvalue())

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
    print(planets)
    planets.sort(key=lambda p: p.dpos)
    # NOTE: We add first planet again to the end in case of clumps near 0/360
    p0 = planets[0]
    p0.dpos += 360
    clumps1 = _pass(planets + [p0])
    planets.sort(key=lambda p: p.dpos, reverse=True)
    clumps2 = _pass(planets)

    print("CLUMPS1")
    print_clumps(clumps1)
    print("CLUMPS2")
    print_clumps(clumps2)

    # TODO: CHECK FOR CLUMPS NEAR 0/360

    clumps = _merge_clumps(clumps1, clumps2)
    print("MERGED CLUMPS")
    print_clumps(clumps)
    clumps = _split_clumps_by_sign(clumps) 
    print("SPLIT BY SIGN")
    print_clumps(clumps)
    # remove singletons
    clumps = [c for c in clumps if len(c) > 1]
    
    return clumps

def _merge_clumps(clumps1, clumps2):
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
    return [list(c) for c in clumps]

def _split_clumps_by_sign(clumps):
    # this is needed for proper rendering in `spread_planets`
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
    print_clumps(clumps)

    for clump in clumps:
        assert len(clump) > 1

        clump.sort(key=lambda p: p.dpos)
        n = len(clump)

        # spread across min distance
        min_distance = len(clump) * theta
        #center_point = _get_center_pt(clump, min_distance)

        print(min_distance)

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
                print("bleeding into previous house")
                bleed_over = 30 - after % 30
                center_point += bleed_over
                center_point += theta / 2 # improve positioning
            
            # check if this causes "bleeding" into *next* house
            before = clump[-1].dpos
            after = center_point + (n / 2) * theta
            # different sign?
            if before // 30 != after // 30:
                print("bleeding into next house")
                bleed_over = after % 30
                center_point -= bleed_over
                center_point -= theta / 2 # improve positioning
        
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

