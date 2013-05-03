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
else:
    # Remove spaces and lowercase console name
    console = ''.join(sys.argv[2].split()).lower()

    # Search IGN for games
    search_url = "http://ign.com/search?q=" + sys.argv[1] + "&page=0&count=10&type=object&objectType=game&filter=games"
    search_soup = BeautifulSoup(requests.get(search_url).text)

    # Find the first page which has the console slug in the URL
    # TODO: make more robust by checking game name somewhere here too
    search_items = search_soup.find("div", class_="search-item")
    game_page = search_items.find("a", href=re.compile(console)).get("href")

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
    review = "[url]" + review_link.get("href") + "[/url]"
else:
    review = "No IGN review found"

# Print everything
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
    print list(para.stripped_strings)[0]
    if i != len(description_paras)-1:
        print ""
print "[/quote]"




