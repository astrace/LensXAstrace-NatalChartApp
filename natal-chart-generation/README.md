# Natal Chart Image Generator

This script generates an image of a natal chart based on the user's birth information. The natal chart image includes the positions of the planets, their corresponding zodiac signs, and the angles (Ascendant and Midheaven) at the time of birth. The generated image has a zodiac wheel with the Ascendant sign in the first house and house numbers overlaid on top.

## Image Generation Algorithm

The image generation algorithm used in this script consists of the following steps:

1. Validate the input data (date, time, and location of birth) and convert it into the required format.
2. Calculate the positions of the planets and angles in the natal chart using the Swiss Ephemeris library.
3. Create Planet objects with their respective positions, absolute positions, and zodiac signs.
4. Create a NatalChart object with the generated list of Planet objects and the Julian day number.
5. Generate the natal chart image by performing the following tasks:
    - Set the background layers (zodiac wheel, house numbers, and logo) based on the user's Ascendant sign.
    - Spread the planets evenly in their respective positions to avoid overlapping.
    - For each planet, add the planet image, the zodiac sign image, and the position text to the background image.
6. Return the generated natal chart image as a PIL Image object.

## File Structure

- `natal_chart.py`: The main script that contains the image generation algorithm and helper functions.
- `constants.py`: Contains constants used in the script, such as image file paths and planet names.
- `image_params.py`: Contains parameters related to the image generation, such as sizes and positions.
- `utils.py`: Contains utility functions for image manipulation, including loading images from local and remote sources.

## Usage

### Local

You can locally generate a natal chart using the CLI. To learn how to use the natal_chart_cli.py script, simply run:
```
./natal_chart_cli.py -h
```
This will generate a natal chart for a person born on January 1st, 2022 at 12:00:00 local time in New York City (latitude 40.7128, longitude -74.0060).


---
------
------
------
------
------
---
---
---
# Astrace Natal Chart Generation

## Testing

We use the unittest and pytest frameworks to create and run test cases for the natal chart generation program. The tests are designed to cover various scenarios, such as:
- natal charts with stelliums
- different background images
- planets near 0/360 degrees on the circle.

Due to the nature of the problem, we rely on **manual visual inspection** of the generated natal chart images to determine if they are rendered correctly. Test results, including comments about any issues, are saved to a log file for further analysis. In case of failed test cases, we provide functionality to retest them at a later time using the data stored in the log file.

### Running tests

[Here's a video](https://www.youtube.com/watch?v=L_4tYsyH3q4) showing the testing workflow (sped up 4x).

---

Basic tests:
```
python -m unittest test_natal_chart.BasicTestNatalChart
```
Visual tests:
```
python -m unittest test_natal_chart.VisualTestNatalChart
```
The test results, along with comments and Unix timestamps for failed cases, will be stored in the `test_results.log` file.

## Natal Chart Rendering Algorithms

### Spreading planets
This is important for rendering things like conjunctions, stelliums, etc (where planets may overlap). See `find_clumps` and `spread_planets` in `utils.py`.

Before/After:
<div>
    <img src="../assets/before.png" alt="Image 1" style="width: 47%; display: inline-block;">
    <img src="../assets/after.png" alt="Image 2" style="width: 47%; display: inline-block;">
</div>

### TODO

<img src="../assets/Screenshot 2023-02-21 at 12.01.30.png" alt="Image 1" style="width: 30%; display: inline-block;">
