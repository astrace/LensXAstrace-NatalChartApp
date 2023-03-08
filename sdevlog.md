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














## References:

1) [Staring venv in VS Code (Linux)](https://www.pythonguis.com/tutorials/getting-started-vs-code-python/#:~:text=To%20use%20a%20virtual%20environment,selecting%20%3E%20Python%3A%20Select%20Interpreter%20.)

2) [My own blog on venv](http://www.cumulativeparadigms.org/wordpress/index.php/2019/03/13/building-a-simple-python-environment-for-data-science-and-development/)

3) [Activate script doesn't appear in venv/bin?](https://stackoverflow.com/questions/41687841/there-is-no-activate-when-i-am-trying-to-run-my-virtual-env)

4) [Install Python 3.9](https://linuxize.com/post/how-to-install-python-3-9-on-ubuntu-20-04/)