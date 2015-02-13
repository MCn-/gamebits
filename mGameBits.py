#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Really early initial implementation of game info grabber - there will be tons of bugs, beware
# MCn

from pyquery import PyQuery as pq
import argparse
import json
import re
import requests
import sys


# Codes used in search urls on MobyGames - add more if necessary
# MG_CONSOLE_CODES = {'pc': 3, 'gb': 10, 'gbc': 11, 'gba': 12}
# MG_CONSOLE_SLUGS = {'N64': 'N64', 'GBA': 'gameboy-advance', 'GBC': 'gameboy-color', 'Dreamcast': 'Dreamcast', 'gamecube': 'gamecube', 'Xbox': 'xbox', 'xbox360': 'xbox360', 'Wii U': 'Wii-u', 'Ps2': 'PS2', 'PS3': 'Ps3','Ps1': 'Playstation', 'genesis': 'genesis', 'android': 'android', 'PC': 'windows', 'nes': 'nes', '3ds': '3ds', 'DS': 'nintendo-ds', 'DSI': 'nintendo-dsi', 'snes': 'snes', 'iphone': 'iphone', 'wii': 'wii', 'mac':'macintosh', 'gameboy': 'gameboy'}


def upload_image(url):
    try:
        # dealing with pesky relative url
        if 'http://' not in url:
            url = 'https://www.mobygames.com/' + url
        # Check for weird url bug where sometimes the image would have two http://
        if '/https://' in url or '/http://' in url:
            url = url[len('https://www.mobygames.com/'):]
        # Remove double slashes
        url = url.replace('com//', 'com/')
        headers = {"Authorization": "Client-ID d656b9b04c8ff24"}
        params = {"image": url}
        r = requests.post("https://api.imgur.com/3/image", headers=headers, params=params)
        return json.loads(r.content)["data"]["link"]
    except:
        return ''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="url of a mobygames game page")
    parser.add_argument("--source", help="source/format of the game")
    parser.add_argument("--language", help="language of the game")
    parser.add_argument("--console", help="the console this game plays on - used for emulator suggestion information", choices=["PS1", "PS2", "NES", "SNES", "N64", "GB", "GBC", "GBA", "GC", "WII", "DS", "DOS"])
    args = parser.parse_args()

    if 'http' in args.url:
        game_page = args.url
    else:
        print 'Search is currently not enabled, it needs to be fixed. Try passing in a URL.'
        return

    page = pq(url=game_page).make_links_absolute()

    proper_game_title = page('.niceHeaderTitle a').eq(0).text()

    date = page('#coreGameRelease a[href*="release-info"]').text()

    # NOTE: u'\xa0' is &nbsp; - replace it with a space
    genre = page('#coreGameGenre a[href*="genre"]').eq(0).text().replace(u'\xa0', ' ')

    review = game_page + '/mobyrank'

    page = pq(url='http://www.mobygames.com/game/windows/dragon-age-origins')
    dirty_description_text = pq(page('h2:contains("Description")').parent().html().replace('<br/>', '\n')).text()
    description_text = re.search(r'Description\s(.*)\s\[ edit', dirty_description_text, re.DOTALL).group(1)

    # Get box art
    game_box_data = page('#coreGameCover img')
    if game_box_data:
        img_url = game_box_data.attr('src').replace('small', 'large')
        imgur_game_box_url = upload_image(img_url)
    else:
        imgur_game_box_url = None

    # Get screenshots
    screenshot_gallery_url = game_page + '/screenshots'
    screenshot_page = pq(url=screenshot_gallery_url).make_links_absolute()
    screenshot_images = screenshot_page('.mobythumbnail img')
    screenshot_one_url, screenshot_two_url = None, None
    if len(screenshot_images) > 0:
        screenshot_one_url = upload_image(screenshot_images.eq(0).attr('src').replace('/s/', '/l/'))
    if len(screenshot_images) > 1:
        screenshot_two_url = upload_image(screenshot_images.eq(1).attr('src').replace('/s/', '/l/'))

    # Print everything
    print "Game Name: " + proper_game_title
    print "Released: " + date
    if args.source:
        print "Source: " + args.source
    if args.language:
        print "Language: " + args.language
    print "Game Genre: " + genre + "\n"

    print "[b]Review:[/b] " + review + "\n"

    print "[b]Description:[/b] "
    print "[quote]"
    print description_text
    print "[/quote]"
    print ""

    if len(sys.argv) > 2:
        # Emulator Suggestion
        if args.console == "PS1":
            print "[b]Emulation:[/b]"
            print "[quote]The best Emulator to use is EPSXE."
            print "http://www.epsxe.com/download.php[/quote]"
        elif args.console == "PS2":
            print "[b]Emulation:[/b]"
            print "[quote]The best Emulator to use is PCSX2."
            print "http://pcsx2.net/download.html[/quote]"
        elif args.console == "NES":
            print "[b]Emulation:[/b]"
            print "[quote]The best Emulator to use is FCEUX."
            print "http://www.fceux.com/web/home.html[/quote]"
        elif args.console == "SNES":
            print "[b]Emulation:[/b]"
            print "[quote]The best Emulator to use is ZSNES."
            print "http://www.zsnes.com/index.php?page=files[/quote]"
        elif args.console == "N64":
            print "[b]Emulation:[/b]"
            print "[quote]The best Emulator to use is Project 64."
            print "http://www.pj64-emu.com/[/quote]"
        elif args.console == "GB":
            print "[b]Emulation:[/b]"
            print "[quote]The best Emulator to use is Virtual Boy Advanced."
            print "http://vba.ngemu.com/downloads.shtml[/quote]"
        elif args.console == "GBC":
            print "[b]Emulation:[/b]"
            print "[quote]The best Emulator to use is Virtual Boy Advanced."
            print "http://vba.ngemu.com/downloads.shtml[/quote]"
        elif args.console == "GBA":
            print "[b]Emulation:[/b]"
            print "[quote]The best Emulator to use is Virtual Boy Advanced."
            print "http://vba.ngemu.com/downloads.shtml[/quote]"
        elif args.console == "GC":
            print "[b]Emulation:[/b]"
            print "[quote]The best Emulator to use is Dolphin."
            print "http://www.dolphin-emulator.com/download.html[/quote]"
        elif args.console == "WII":
            print "[b]Emulation:[/b]"
            print "[quote]The best Emulator to use is Dolphin."
            print "http://www.dolphin-emulator.com/download.html[/quote]"
        elif args.console == "DS":
            print "[b]Emulation:[/b]"
            print "[quote]The best Emulator to use is DSEmu."
            print "http://dsemu.oopsilon.com/[/quote]"
        elif args.console == "DOS":
            print "[b]Emulation:[/b]"
            print "[quote]The best Emulator to use is DOSBox."
            print "http://www.dosbox.com/download.php?main=1[/quote]"

    if screenshot_one_url:
        print "\n[b]Screenshots:[/b]\n"
        print "[img]{0}[/img]".format(screenshot_one_url)
    if screenshot_two_url:
        print "[img]{0}[/img]".format(screenshot_two_url)
    if screenshot_one_url:
        print "Screenshot gallery: " + screenshot_gallery_url

    if imgur_game_box_url:
        print "\n\nCover image: " + imgur_game_box_url

    print "\n-------------------------------------------------\n"


if __name__ == '__main__':
    main()
