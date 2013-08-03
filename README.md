gamebits
========

Fetch game info from the internet. There will be lots of bugs, please submit any issues here or on the forums. Or PM me.

Installation
============

- Download the files from https://github.com/MCn-/gamebits/archive/mGameBits.zip
- Install pip: http://www.pip-installer.org/en/latest/installing.html
    - If you're not sure how to do this, install setuptools (http://pythonhosted.org/setuptools/easy_install.html#installing-easy-install) and run ``easy_install pip`` on the command line.
    - If you're really struggling, have a look at https://sites.google.com/site/pydatalog/python/pip-for-windows (not used myself, but seems promising)
    - If easy_install or pip aren't being found, try adding the python folders to your path: http://www.anthonydebarros.com/2011/10/15/setting-up-python-in-windows-7/ **point 3**
- (Optional: use a virtualenv)
- Once pip is installed, ``cd`` to the gamebits/ directory (that you just downloaded from github!) and run ``pip install -r requirements.txt``. This will download all dependencies automatically.
- Put gamebits.py in a folder somewhere, optionally add it to your path

Usage
========

You can run the script by supplying either a URL to a MobyGames game page or simply the game name.

    ./gamebits.py <GAME NAME> <CONSOLE> <SOURCE> <LANGUAGE>

or

    ./gamebits.py <MG URL> <CONSOLE> <SOURCE> <LANGUAGE>
    
Note: CONSOLE should be equal to the one used on MG, which usually will be fairly similar to what you would expect, but in some cases may be different. For example, the Nintendo 64 has an id of n64. I recommend just trying it and seeing what happens: it will probably work in 99% of cases without much thought.
    
