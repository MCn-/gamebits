gamebits
========

Fetch game info from the internet. There will be lots of bugs, please submit any issues here or on the forums. Or PM me.

Installation
============

- Download the files from https://github.com/MCn-/gamebits/archive/mGameBits.zip
- Install python 2, which should come with pip
- (Optional: use a virtualenv)
- Once pip is installed, ``cd`` to the gamebits/ directory (that you just downloaded from github!) and run ``pip install -r requirements.txt``. This will download all dependencies automatically.
- Put mGameBits.py in a folder somewhere, optionally add it to your path

Usage
========

**This may not be accurate. Run mGameBits -h to see the required arguments.**

You can run the script by supplying either a URL to a MobyGames game page or simply the game name.

    ./mGameBits.py <GAME NAME> <CONSOLE> <SOURCE> <LANGUAGE>

or

    ./mGameBits.py <MG URL> [<CONSOLE>] [<SOURCE>] [<LANGUAGE>]

Note: CONSOLE should be equal to the one used on MG, which usually will be fairly similar to what you would expect, but in some cases may be different. For example, the Nintendo 64 has an id of n64. I recommend just trying it and seeing what happens: it will probably work in 99% of cases without much thought.

