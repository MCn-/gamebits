#!/usr/bin/env python

# Really early initial implementation of game info grabber - there will be tons of bugs, beware
# MCn

from bs4 import BeautifulSoup
import requests
import sys, re

# TODO: nicer errors on bad inputs
# TODO: youtube video functionality
# TODO: take a list file and run on each element
# TODO: supply required libraries

# Get URL if none supplied
if "http" in sys.argv[1]:
    game_page = sys.argv[1]
    game_name = ""
else:
    game_name = sys.argv[1]

    # Remove spaces and lowercase console name
    console = '-'.join(sys.argv[2].split()).lower()

    # Search IGN for games
    search_url = "http://ign.com/search?q=" + sys.argv[1] + "&page=0&count=10&type=object&objectType=game&filter=games"
    search_soup = BeautifulSoup(requests.get(search_url).text)

    # Find the page for the game
    search_items = search_soup.find_all("div", class_="search-item-title")

    the_tag = None
    found_names = []
    for item in search_items:
        if item.a and item.a.em:
            item.a.em.unwrap()

        found_names.append(item.a.text.strip());
        if sys.argv[1] == item.a.text.strip():
            the_tag = item

    if not the_tag:
        print "Error: No game by the name " + sys.argv[1] + " was found in the IGN search results: either try adjusting the name or use the direct URL instead.\n"
        print "The following games were found on the search results page: "
        for name in found_names:
            print " - " + name
        sys.exit()

    for item in search_items:
        if item.a and item.a.em:
            item.a.em.unwrap()
        if sys.argv[1] == item.a.text.strip():
            the_tag = item

    if console in the_tag.a.get("href"):
        game_page = the_tag.a.get("href")
    else:
        game_page = the_tag.parent.find(class_="search-item-sub-title").find("a", href=re.compile(console)).get("href")

# Open URL
soup = BeautifulSoup(requests.get(game_page).text)

# Source and language args
source = sys.argv[3]
language = sys.argv[4]

# Get the gameinfo div, useful for several bits of data
gameinfo = soup.find("div", class_="gameInfo")

# Find the release date tag, jump up to parent and format it
date = list(gameinfo.find(text=re.compile("Release Date")).parent.parent.stripped_strings)[1].strip(": ")

# Similarly for genre
genre = list(gameinfo.find("a", href=re.compile("genre")).stripped_strings)[0]

# Search for a review link
review_link = soup.find("a", title="review")
if review_link:
    review = review_link.get("href")
else:
    review = "No IGN review found"

# Print everything
print "Game Name: " + game_name
print "Released: " + date
print "Source: " + source
print "Language: " + language
print "Game Genre: " + genre + "\n"

print "IGN Review: " + review + "\n"

print "Description: "
# Print out all the paragraphs for the description
print "[quote]"
description_paras = gameinfo.find_all("p")
for i, para in enumerate(description_paras):
    if len(list(para.stripped_strings)) > 0:
        print list(para.stripped_strings)[0]
        if i != len(description_paras)-1:
            print ""
    else:
        print "No description available"
        break
print "[/quote]"
print ""

# Emulator Suggestion
print "Emulation:"
if sys.argv[2] == "PS":
	print "[quote]The best Emulator to use is EPSXE."
	print "http://www.epsxe.com/download.php[/quote]"
elif sys.argv[2] == "PS2":
	print "[quote]The best Emulator to use is PCSX2."
	print "http://pcsx2.net/download.html[/quote]"
elif sys.argv[2] == "NES":
	print "[quote]The best Emulator to use is FCEUX."
	print "http://www.fceux.com/web/home.html[/quote]"
elif sys.argv[2] == "SNES":
	print "[quote]The best Emulator to use is ZSNES."
	print "http://www.zsnes.com/index.php?page=files[/quote]"
elif sys.argv[2] == "N64":
	print "[quote]The best Emulator to use is Project 64."
	print "http://www.pj64-emu.com/[/quote]"
elif sys.argv[2] == "GB":
	print "[quote]The best Emulator to use is Virtual Boy Advanced."
	print "http://vba.ngemu.com/downloads.shtml[/quote]"
elif sys.argv[2] == "GBC":
	print "[quote]The best Emulator to use is Virtual Boy Advanced."
	print "http://vba.ngemu.com/downloads.shtml[/quote]"
elif sys.argv[2] == "GBA":
	print "[quote]The best Emulator to use is Virtual Boy Advanced."
	print "http://vba.ngemu.com/downloads.shtml[/quote]"
elif sys.argv[2] == "GC":
	print "[quote]The best Emulator to use is Dolphin."
	print "http://www.dolphin-emulator.com/download.html[/quote]"
elif sys.argv[2] == "WII":
	print "[quote]The best Emulator to use is Dolphin."
	print "http://www.dolphin-emulator.com/download.html[/quote]"
elif sys.argv[2] == "DS":
	print "[quote]The best Emulator to use is DSEmu."
	print "http://dsemu.oopsilon.com/[/quote]"
elif sys.argv[2] == "DOS":
	print "[quote]The best Emulator to use is DOSBox."
	print "http://www.dosbox.com/download.php?main=1[/quote]"
else:
	print "[quote]No Emulator information[/quote]"
