IMAGES_URL = 'https://d1tswrzvc9aaiy.cloudfront.net/images/'

#Note: BACKGROUND_FILES was not used anywhere. Constant has
#been modified to accomidate a backgrounds folder.
BACKGROUND_FILES_PATH = "./assets/images/"
#Actually a dictionary...but importing the Enum module is an extra dependency.
BACKGROUND_FILES_ENUM = {
    1:"deepred.png",
    2:"emeraldgreen.png",
    3:"gold.png",
    4:"salmonpink.png",
    5:"skyblue.png",
    6:"sunsetorange.png",
    7:"teal.png",
    8:"violet.png",
}

SIGNS = ['Ari', 'Tau', 'Gem', 'Can', 'Leo', 'Vir', 'Lib', 'Sco', 'Sag', 'Cap', 'Aqu', 'Pis']

# values are "body numbers" as defined in swisseph
PLANET_NAMES = {
    "Sun": 0,
    "Moon": 1,
    "Venus": 2,
    "Mars": 3,
    "Jupiter": 4,
    "Saturn": 5,
    "Uranus": 6,
    "Neptune": 7,
    "Pluto": 8,
    "North Node": 11,
    "Chiron": 16,
}
