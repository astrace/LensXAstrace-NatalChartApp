from PIL import Image

asset_img_path = "./assets/images/"
bg_dims = (2203,2203)
color_dict = {"gold":(255,215,0), "teal":(0,128,128), "emeraldgreen":(0,130,100),
              "skyblue":(72,180,224),"salmonpink":(250,128,114),"deepred":(175,0,0),
              "sunsetorange":(253,94,83),"violet":(74,20,140)}

def gen_solid_color_img(dims,color):
    """
        Generate a solid colour image with PIL

        Arguments:
            - dims: An (x,y) 2-ple that gives with width and height of image
            - color: A string represnting a colour name - use color_dict to resolve to 3-ple.

        Notes: Code taken from: https://stackoverflow.com/questions/38900511/how-to-create-a-new-color-image-with-python-imaging
    """
    img = Image.new("RGB", dims, color_dict[color])
    #img.show()
    img.save(asset_img_path + color + ".png")

#For now, just call functions you want from here.
if __name__ == "__main__":
    for color in color_dict.keys():
        gen_solid_color_img(bg_dims,color)
