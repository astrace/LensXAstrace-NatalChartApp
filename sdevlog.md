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












## References:

1) [Staring venv in VS Code (Linux)](https://www.pythonguis.com/tutorials/getting-started-vs-code-python/#:~:text=To%20use%20a%20virtual%20environment,selecting%20%3E%20Python%3A%20Select%20Interpreter%20.)

2) [My own blog on venv](http://www.cumulativeparadigms.org/wordpress/index.php/2019/03/13/building-a-simple-python-environment-for-data-science-and-development/)

3) [Activate script doesn't appear in venv/bin?](https://stackoverflow.com/questions/41687841/there-is-no-activate-when-i-am-trying-to-run-my-virtual-env)

4) [Install Python 3.9](https://linuxize.com/post/how-to-install-python-3-9-on-ubuntu-20-04/)