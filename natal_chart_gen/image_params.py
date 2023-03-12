"""
Parameters for image generation - chosen to give proper spacing,
make the images look good, etc. These are subject to change for future
versions of the application.

NOTE: In most instances, params are a function of background image 
height/width in order to minimize "degrees of freedom"
"""

# distance of objects (planet, sign, text)
# from center as % of background image
PLANET_RADIUS = 0.295
TEXT_RADIUS = 0.263
SIGN_RADIUS = 0.235

# obj size as % of background image
PLANET_SIZE = 0.055
# !important NOTE: TEXT_SIZE is in pixels.
TEXT_SIZE = 30 
SIGN_SIZE = 0.040

# radius of inner circle containing house numbers
HOUSE_NUMBER_RADIUS = 0.45

# radius of central astrace logo
LOGO_RADIUS = 0.07
