## Sean's Dev Log

#### Getting Python venv running in VS Code (Linux):

The following posts were referenced: [1] [2] [3]. venv was installed at the root of the directory. Had to install
python3.8-venv with apt to get this to work correctly (error).

```
python3.X -m venv .astrenv

source .astrenv/bin/activate

pip3 -r ./natal_chart_gen/requirements.txt
```

#### Kerykeion requires python 3.9...

Install Python 3.9 the easy way [4]. Reconfigure all of the stuff above.

All directories installed OK when running `pip install -r requirements.txt`

#### Running prototype.py

Encountered the following error: Filenotfound: North Node.png. It turns out that this file was called "north node". I corrected the case of the file name, and the script worked.

Curiously, when python outputs the image, it gets passed to my Pinta program and is opened up in it, for display (system default)?

#### Code Investigation and Documentation:

We have **four major** files in our Python Backend:

1) **Prototype:** Contains the main method, and outputs a Natal Chart. Contains Planet and Natal Chart objects. generate() and its hidden helper _generate() do the main body of work. Other support functions that perform PIL operations, plane geometry, etc are also placed here.

2) **Utils:** Contains helper functions to upload/download generated charts to Amazon S3 buckets (using the boto library). Contain's Sasa's "clumping" algorithm, that spreads out planet-sign clusters that overfill a particular natal chart house. 

3) **App:** A smaller file contains one function: lambda_handler(). This calls prototype.generate() and then posts the output to the Amazon S3 Bucket. This is essentially middle-ware.

4) **Test:** Our testing file. Just a main method python script. No frameworks currently.

And **two minor** files:

1) Constants: Basic URLS, file names, etc used throughout the application.

2) Image_Params: A file that contains numerical values, to make the generated images look nice.

Formatting of Comments:

- ChatGPT was used to generate strings. The strings were then checked for accuracy, and then trimmed down to take up less space.
- Some rules to format the strings:
    - Keep the convention that Chat GPT has used.
    - The "Notes" subsections are usually low information, integrate them into the other sections unless absolutely necessary.
    - The One-Line Summary that ChatGPT generates is often omitted. For example, the purpose of <class Planet> is just obvious from it's name.
    - String placed after the functional signatures, using triple quotes.
    - Trivial functions don't have Docstrings (example: utils.print_clumps()).

#### Random Background Feature:

We have *N* possible backgrounds, and wish to randomly select one for one of our natal charts. For simplicity, assume that the probability of choosing any background is equiprobable (so $ \thicksim \tfrac{1}{N}$).

TODO:

1) Make a simple script to use PIL to generate 2203px x 2203px solid colour pngs. Make 8 pngs. Colours: gold, teal, emeraldgreen, skyblue, salmonpink, deepred, sunsetorange, seagreen. Format the backgrounds with the names <color/shade name>.png.

2) Changing the generation code:

- We would like a random background to be selected, when generating our Natal Chart. Where are backgrounds referencedin utils, prototype and other places?

Prototype.py:
    - _generate()
    - function def: set_background()

Constants.py:
    - BACKGROUND_FILE constant
        - This isn't used in prototype.
        - Modify it to be BACKGROUND_FILES_PATH

When we run generate(), we are currently loading from a local setup (local=True). We actually have a load_image_fn that is passed through the calls, as a form of polymorphism. This depends on whether we call the image generation locally, or externally.
- We have to keep the function passing between generate, _generate and set_background(). **This should not be tampered with.**

For the purposes of this code sprint, our load_image function is as follows:

```
lambda filename: Image.open("assets/images/" + filename) 

```
**Where do we place the randomization code?** 

We make a separate function that takes a dictionary of values-filenames, and calls a randomization routine. This way, other functions (such as for forelayer selection) can also call this routine.


#### Revisions to randomization codes:

- Our dictionary has been modified to have filename:probability pairs.
- We treat our discrete probabilities as domains in the [0,1] continuum In theory, it does not matter how the domains are arranged. So we just traverse the list in the order they appear.
- Note that this solution is imperatively programmed. We could import numpy/scipy, or build lots of constructs. This solution is not elegant, but it relatively terse+efficient and does the job.

- Note: As per:https://stackoverflow.com/questions/835092/python-dictionary-are-keys-and-values-always-the-same-order we can assume that keys() and values() will always return in the same order (the order of definition or insertion), assuming our dictionary is never altered. As it is predefined, this cannot change.

#### How to update my current branch, from the origin remote?

If you have already pushed your current branch to origin, just use:

```
git pull
```


## References:

1) [Staring venv in VS Code (Linux)](https://www.pythonguis.com/tutorials/getting-started-vs-code-python/#:~:text=To%20use%20a%20virtual%20environment,selecting%20%3E%20Python%3A%20Select%20Interpreter%20.)

2) [My own blog on venv](http://www.cumulativeparadigms.org/wordpress/index.php/2019/03/13/building-a-simple-python-environment-for-data-science-and-development/)

3) [Activate script doesn't appear in venv/bin?](https://stackoverflow.com/questions/41687841/there-is-no-activate-when-i-am-trying-to-run-my-virtual-env)

4) [Install Python 3.9](https://linuxize.com/post/how-to-install-python-3-9-on-ubuntu-20-04/)

5) [Upload New Branch to Remote](https://stackoverflow.com/questions/2765421/how-do-i-push-a-new-local-branch-to-a-remote-git-repository-and-track-it-too)

6) [Update your current branch from more recent origin](https://stackoverflow.com/questions/11278497/update-a-local-branch-with-the-changes-from-a-tracked-remote-branch)