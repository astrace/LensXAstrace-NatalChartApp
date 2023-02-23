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
                # if it's the first planet, add it to current (empty) clump
                # or, if it satisfies the clump criteria, add it to the current clump
                curr_clump.append(p)
            else:
                clumps.append(curr_clump)
                curr_clump = [p]

        clumps.append(curr_clump)
        return clumps

    # hard to explain why this needs to be done twice: forward & backwards pass
    # ... there are edge cases where one pass fails
    clumps1 = _pass(sorted(planets, key=lambda p: p.dpos))
    clumps2 = _pass(sorted(planets, key=lambda p: p.dpos, reverse=True))

    # check to see if there's a clump near 0 / 360
    # Note: only needs to be done on first set of clumps
    if _clump_check(
            clumps1[0][0].dpos,
            clumps1[-1][-1].dpos,
            len(clumps1[0]) + len(clumps1[-1])
        ):
        # merge
        clumps1[0] = clumps1[-1] + clumps1[0]
        clumps1 = clumps1[:-1]
    
    clumps = remove_singletons_and_merge_clumps(clumps1, clumps2)
    
    return clumps

def remove_singletons_and_merge_clumps(clumps1, clumps2):
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

    print('CLUMPS')
    print_clumps(clumps)

    for clump in clumps:
        n = len(clump)
        if n == 1:
            continue
        # spread across min distance
        min_distance = len(clump) * theta
        center_point = (clump[0].dpos + clump[-1].dpos) / 2
        if len(clump) > 5:
            # center point should be in center of sign
            center_point = center_point - center_point % 30 + 15 + theta / 2
        new_positions = np.arange(
            center_point - (n / 2) * theta,
            center_point + (n / 2) * theta,
            theta
        )
        # set display positions
        clump.sort(key=lambda p: p.dpos)
        for (p, pos) in zip(clump, new_positions):
            p.dpos = pos

def print_clumps(clumps):
    for c in clumps:
        print([str(p) for p in c])



