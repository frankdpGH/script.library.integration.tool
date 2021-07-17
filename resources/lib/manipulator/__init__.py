#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Module dedicate to manipulate title."""

import os
import re

# TODO: Use combined list on all platforms. Would need to be combined with version check
# to re-add all managed items
MAPPED_STRINGS = {
    r' \[cc\]': ' ',
    r'\(Legendado\)': ' ',
    r'\(Leg\)': ' ',
    r'\(Dub.+?\)': ' ',
    r'\(.+? Dub\)': ' ',
    r'\((Dublagens|Dubbing) (International|Internacionais)\)': ' ',
    r'\((Dublado|Dubbed) .+?\)': ' ',
    r'\s{1,3}S\d{1,5}\s{1,3}': ' ',
    r'\s{1,4}\#\d{1,6}\s{1,4}\-\s{1,4}': ' ',
    r'\.': ' ',
    r'\:': ' ',
    r'\/': ' ',
    r'\"': ' ',
    r'\$': ' ',
    r'é': 'e',
    # r'Part 1': 'Part One',
    # r'Part 2': 'Part Two',
    # r'Part 3': 'Part Three',
    # r'Part 4': 'Part Four',
    # r'Part 5': 'Part Five',
    # r'Part 6': 'Part Six',
    r'Final Season': ' ',
    r'\s{1,10}': ' ',
}

if os.name == 'nt':
    MAPPED_STRINGS += {
        '?': ' ',
        '<': ' ',
        '>': ' ',
        '\\': ' ',
        '*': ' ',
        '|': ' ',
    }

    # [
    #('+', ''),
    #(',', ''),
    #(';', ''),
    #('=', ''),
    #('[', ''),
    #(']', ''),
    # ]

# TODO: NETFLIX find a way to deal with show with Part 1,
# Part 2 and etc, now, any part will be a season,
# maybe a api call with trakt or tvdb to get episode info is a way


class Cleaner(object):
    """Class with methods to clear strings from content."""

    def __init__(self) -> None:
        """Cleaner __init__."""
        super().__init__()
        self.strings = MAPPED_STRINGS

    def showtitle(self, showtitle):
        """Function to remove strings from showtitle."""
        for key, val in self.strings.items():
            showtitle = re.sub(key, val, str(showtitle))
        return showtitle.strip()

    def title(self, title, showtitle=None):
        """Function to remove strings and showtitle from title."""
        for key, val in self.strings.items():
            title = re.sub(key, val, str(title))
        return title.replace(self.showtitle(showtitle), ' ').strip()


