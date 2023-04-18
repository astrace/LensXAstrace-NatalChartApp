import json
import math
import os
import random
import subprocess
import sys
import time
import unittest
from datetime import datetime, timedelta
from os.path import dirname, abspath

# Add the grandparent directory to the sys.path
grandparent_dir = dirname(dirname(abspath(__file__)))
sys.path.insert(0, grandparent_dir)

import numpy as np
import warnings
# Suppress the ResourceWarning
warnings.filterwarnings("ignore", category=ResourceWarning)

import constants
import _utils
import utils

from constants import IMG_DIR, IMG_FILES
from image_params import PLANET_SIZE, PLANET_RADIUS
IMG_DIR = '../' + IMG_DIR
from natal_chart import NatalChart, _generate


class BasicTestNatalChart(unittest.TestCase):
    m = len(NatalChart.required_objects)
    theta = math.degrees(2 * math.asin(0.5 * (PLANET_SIZE / 2) / PLANET_RADIUS))

    def test_find_clumps_one_clump(self):
        chart = _utils.create_mock_natal_chart([0] * self.m)
        clumps = utils.find_clumps(list(chart.objects.values()), self.theta)
        assert len(clumps) == 1 and set(clumps[0]) == set(chart.objects.values())

    def test_find_clumps_none(self):
        positions = np.arange(0, 360, 360 / self.m) # perfectly evenly spaced out
        chart = _utils.create_mock_natal_chart(positions)
        clumps = utils.find_clumps(list(chart.objects.values()), self.theta)
        assert len(clumps) == self.m

    def test_find_clumps_near_zero(self):
        positions = [0] * (self.m // 2) + [358] * (self.m // 2) + [30] * (self.m % 2)
        chart = _utils.create_mock_natal_chart(positions)
        clumps = utils.find_clumps(list(chart.objects.values()), self.theta)
        assert len(clumps) == 3

    def test_find_clumps_one_far_away(self):
        # NOTE: Example why 2 passes is necessary !!!
        positions = [45] * (self.m - 2) + [59] + [30]
        chart = _utils.create_mock_natal_chart(positions)
        clumps = utils.find_clumps(list(chart.objects.values()), self.theta)
        assert len(clumps) == 1 and len(clumps[0]) == self.m

# Test class
class VisualTestNatalChart(unittest.TestCase):
    image_loader = utils.LocalImageLoader(IMG_DIR, IMG_FILES)
    bg_im_size = image_loader.load_all_images()
    image_loader.resize_all_images()
    unixtime = int(time.time())

    def test_natal_charts_with_stelliums(self):
        for _ in range(20):
            n = random.randint(2, 10)
            chart = _utils.generate_stellium(n)
            self.visual_test(chart)

    def test_natal_charts_with_backgrounds(self):
        bg_images = constants.IMG_FILES['BACKGROUNDS'].keys()
        for bg_im_file in bg_images:
            chart = _utils.random_chart()
            self.visual_test(chart, bg_im_file)

    def test_natal_charts_near_zero_degrees(self):
        for _ in range(10):
            n = random.randint(2, 10)
            chart = _utils.generate_stellium_near_zero_degrees(n)
            self.visual_test(chart)

    def visual_test(self, natal_chart_obj, bg_file=None):
        im = _generate(natal_chart_obj, self.image_loader, bg_file)
        
        # Visually inspect the generated image
        temp_img_path = "temp_image.png"
        im.save(temp_img_path)

        viewer_command = "open" if sys.platform == "darwin" else "xdg-open"
        viewer_process = subprocess.Popen([viewer_command, temp_img_path])

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
                    "positions": natal_chart_obj.positions(),
                    "comment": comment,
                    "unixtime": self.unixtime
                }
                # Prettify JSON output with an indentation of 2 spaces
                #pretty_json = json.dumps(test_case, indent=2)
                #log_file.write(pretty_json + "\n")
                log_file.write(json.dumps(test_case) + "\n")

# Functions for retesting failed test cases
# TODO: Create command for running this
def retest_failed_cases(log_file_path):
    failed_test_cases = []

    with open(log_file_path, "r") as log_file:
        for line in log_file:
            test_case = json.loads(line.strip())
            failed_test_cases.append(test_case)

    for test_case in failed_test_cases:
        print(f"Retesting failed case: {test_case['positions']}")
        print(f"Previous comment: {test_case['comment']}")
        test_instance = TestNatalChart()
        chart = _utils.create_mock_natal_chart(test_case["positions"])
        test_instance.visual_test(chart)


if __name__ == "__main__":
    unittest.main()

