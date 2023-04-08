import sys
import json
import os
import random
import subprocess
import time
import unittest
from datetime import datetime, timedelta
from os.path import dirname, abspath

# Add the grandparent directory to the sys.path
grandparent_dir = dirname(dirname(abspath(__file__)))
sys.path.insert(0, grandparent_dir)

import warnings
# Suppress the ResourceWarning
warnings.filterwarnings("ignore", category=ResourceWarning)

import constants
import _utils
import utils

from constants import IMG_DIR, IMG_FILES
IMG_DIR = '../' + IMG_DIR
from natal_chart import _generate

# Test class
class TestNatalChart(unittest.TestCase):
    image_loader = utils.LocalImageLoader(IMG_DIR, IMG_FILES)
    bg_im_size = image_loader.load_all_images()
    image_loader.resize_all_images()
    unixtime = int(time.time())

    @unittest.skip("suppress")
    def test_natal_charts_with_stelliums(self):
        for _ in range(3):
            n = random.randint(2, 10)
            chart = _utils.generate_stellium(n)
            self.visual_test(chart)

    @unittest.skip("suppress")
    def test_natal_charts_with_backgrounds(self):
        bg_images = constants.IMG_FILES['BACKGROUNDS'].keys()
        for bg_im_file in bg_images:
            chart = _utils.random_chart()
            self.visual_test(chart, bg_im_file)

    @unittest.skip("suppress")
    def test_natal_charts_near_zero_degrees(self):
        for _ in range(3):
            n = random.randint(2, 10)
            chart = _utils.generate_stellium_near_zero_degrees(n)
            self.visual_test(chart)

    @unittest.skip("suppress")
    def test_basic_cases(self):
        tuple_list = [
            ([20,40,60,80,100,120,140,160,180,200,220,240,260],"basic singletons"),
            ([10,10,50,50,90,90,130,130,170,170,240,240,300],"basic pairs"),
            ([40,40,40,120,120,120,200,200,200,250,250,250,320],"basic triplets"),
            ([200,200,200,200,200,200,200,200,200,300,300,300,300],"9 planet stellium"),
            ([150,150,150,150,150,150,150,150,150,150,150,150,150],"everything in one house"),
            ]
        self.manual_test(tuple_list)

    @unittest.skip("suppress")
    def test_boundary_straddle(self):
        tuple_list = [
            ([1,1,60,120,120,120,200,200,200,250,290,358,358],"singleton's straddling"),
            ([1,1,60,120,120,120,200,200,200,250,290,358,358],"pairs straddling"),
            ([1,1,1,120,120,120,200,200,200,250,358,358,358],"triplets straddling"), 
            ([1,1,1,1,120,120,120,120,200,357,358,358,358],"groups of four straddling"), 
            ([1,1,1,2,2,200,200,200,356,357,358,358,358],"groups of five"), 
            ([1,1,1,2,2,2,200,356,356,357,358,358,358],"groups of six"), 
        ]
        self.manual_test(tuple_list)

    def test_boundary_overlap(self):
        tuple_list = [
            ([0, 45, 90, 90, 130, 130, 170,170, 240, 240, 300, 345, 359],"pair of two over boundary"),
            ([0, 1, 120, 120, 120, 200, 200, 200, 200, 340, 340, 340, 359],"group of three over boundary"),
            ([0, 1, 120, 120, 120, 200, 200, 200, 200, 340, 340, 358, 359],"group of four over boundary"),
            ([0, 1, 1, 120, 120, 200, 200, 200, 200, 340, 340, 358, 359],"group of five over boundary")
            ([0, 1, 1, 120, 120, 200, 200, 200, 200, 340, 357, 358, 359],"group of six over boundary")
            ([0,0,1,1,1,250,250,250,250,358,359,359,359],"group of nine over boundary"),
        ]
        self.manual_test(tuple_list)

    def test_non_boundary_overlaps(self):
        tuple_list = [
            ([10,20,30,40,50,50,53,53,105,150,200,230,280],"pair of two overlap interior"),
            ([10,20,30,50,50,50,53,53,53,150,200,230,280],"pair of three overlap interior"),
            ([10,20,50,50,50,50,53,53,53,53,200,230,280],"pair of four overlap interior"),
            ([10,50,50,50,50,50,53,53,53,53,53,230,280],"pair of five overlap interior"),
            ([50,50,50,50,50,50,53,53,53,53,53,53,280],"pair of six overlap interior"),
            ([50,50,50,50,50,50,53,53,53,53,53,53,53],"pair of six and seven overlap interior"),
        ]
        self.manual_test(tuple_list)

    @unittest.skip("suppress")
    def test_pathologic_cases(self):
        tuple_list = [
            ([100,100,100,110,110,110,120,120,120,130,130,130,130],"multi group interior overlap"),
            ([357, 357, 358, 358, 359, 359, 0, 0, 0, 1, 1, 1, 2],"everything over the boundary"),
            ([1, 1, 1, 1, 1, 1, 1, 1, 1, 358, 358, 358, 358],"group of nine and four over boundary"),
            ([358, 359, 359, 0, 0, 1, 7, 7, 7, 7, 7, 7, 7],"group of six and seven over boundary"),
            ([2,2,2,12,12,12,348,348,348,348,358,358,358],"multi groups, all near the boundary"),
        ]
        self.manual_test(tuple_list)

    def manual_test(self,tuple_list):
        """
            Helper function to reduce redundant code in test case groupings.
            Tests are described as "manual", because we specify a list of planet positions directly.

            Args:
                - tuple_list: a list of 2-ples, that contain a list of planet positions [0], and test description [1].
        
        """
        for tup in tuple_list:
            chart = _utils.create_mock_natal_chart(tup[0])
            self.visual_test(chart,None,tup[1])

    def visual_test(self, natal_chart_obj, bg_file=None, test_desc=""):
        """
            This method allows for user interactivity when sequentially genearating test images.
            The user can record notes for observed failures in charts, and read them in a file later on.

            Args:
                - natal_chart_obj
                - bg_file: specify a bg_file to use directly.
                - test_desc: Optional test_description field for the test log file.
        """
        im = _generate(natal_chart_obj, self.image_loader, bg_file)
        
        # Visually inspect the generated image
        temp_img_path = "temp_image.png"
        im.save(temp_img_path)

        viewer_command = "open" if sys.platform == "darwin" else "xdg-open"
        viewer_process = subprocess.Popen([viewer_command, temp_img_path])

        if (test_desc != ""):
            print("Running Test: " + test_desc)

        is_correct = input("Is the image correct? (y/n) ")

        # Close the image and terminate the viewer process
        viewer_process.terminate()
        viewer_process.wait()
        os.remove(temp_img_path)
        im.close()
        
        if is_correct == 'n':
            comment = input("Please provide a comment on the issue: ")
            # Save the test case result and comment to a log file
            with open("test_results.log", "a") as log_file:
                test_case = {
                    "test_class": self.__class__.__name__,
                    "test_desc": test_desc,
                    "positions": natal_chart_obj.positions(),
                    "comment": comment,
                    "unixtime": self.unixtime
                }
                # Prettify JSON output with an indentation of 2 spaces
                #pretty_json = json.dumps(test_case, indent=2)
                #log_file.write(pretty_json + "\n")
                log_file.write(json.dumps(test_case) + "\n")

def retest_failed_cases(log_file_path):
    """
        This function scans the test_results.log file, and loads all failed tests that are logged there.
        It allows us to tweak code and patch failed tests more quickly.
    """

    failed_test_cases = []

    with open(log_file_path, "r") as log_file:
        for line in log_file:
            test_case = json.loads(line.strip())
            failed_test_cases.append(test_case)

    for test_case in failed_test_cases:
        print(f"Retesting failed case: {test_case['positions']}")
        print(f"Test Description: {test_case['test_desc']}")
        print(f"Previous comment: {test_case['comment']}")
        test_instance = TestNatalChart()
        chart = _utils.create_mock_natal_chart(test_case["positions"])
        test_instance.visual_test(chart)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "retest":
        retest_failed_cases("test_results.log")
    else:
        unittest.main()