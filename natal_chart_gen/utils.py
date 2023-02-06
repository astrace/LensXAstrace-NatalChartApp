import requests
from io import BytesIO

import boto3
from PIL import Image

import constants

def load_image(filename):
    url = constants.IMAGES_URL + filename
    print("Loading {} ...".format(url))
    resp = requests.get(url)
    im = Image.open(BytesIO(resp.content))
    return im

def read_image_from_s3(bucket, key, region_name='us-east-1'):
    """Load image file from s3.

    Parameters
    ----------
    bucket: string
        Bucket name
    key : string
        Path in s3

    Returns
    -------
    np array
        Image array
    """
    print('Reading {} from S3 bucket {} ...'.format(key, bucket))
    s3 = boto3.client('s3')
    file_byte_string = s3.get_object(Bucket=bucket, Key=key)['Body'].read()
    x = BytesIO(file_byte_string)
    return Image.open(BytesIO(file_byte_string))
    
def write_image_to_s3(im, bucket, key, region_name='us-east-1'):
    """Write an image array into S3 bucket

    Parameters
    ----------
    im: PIL.Image.Image
        Image
    bucket: string
        Bucket name
    key : string
        Path in s3

    Returns
    -------
    None
    """
    s3 = boto3.resource('s3', region_name)
    bucket = s3.Bucket(bucket)
    object = bucket.Object(key)
    file_stream = BytesIO()
    im.save(file_stream, format='png')
    object.put(Body=file_stream.getvalue())

def find_clumps(planets, theta):
    # TODO: explain what `theta` is
    # returns list of lists
    # - sort planets according to location on perimeter
    planets.sort(key=lambda p: p.display_pos)
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
        if i == 0 or _clump_check(curr_clump[0].display_pos, p.display_pos, 1 + len(curr_clump)):
            curr_clump.append(p)
            
        else:
            clumps.append(curr_clump)
            curr_clump = [p]
        
        i += 1
        
    clumps.append(curr_clump)
    
    # final check to see if there's a clump near 0 / 360
    first_planet_pos = clumps[0][0].display_pos
    last_planet_pos = clumps[-1][-1].display_pos
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
    theta = math.degrees(2 * math.asin(0.5 * (PLANET_SIZE / 2) / PLANET_RADIUS)) 
    
    clumps = find_clumps(planets, theta)
    
    for clump in clumps:
        n = len(clump)
        if n == 1:
            continue
        print("CLUMP:", [(p.name, p.display_pos) for p in clump])
        # spread across min distance
        min_distance = len(clump) * theta
        center_point = (clump[0].display_pos + clump[-1].display_pos) / 2
        new_positions = np.arange(
            center_point - (n / 2) * theta,
            center_point + (n / 2) * theta,
            theta
        )
        # set display positions
        for (p, pos) in zip(clump, new_positions):
            print(p.name, p.abs_pos, pos)
            p.display_pos = pos
    
