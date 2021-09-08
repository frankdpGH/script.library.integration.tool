# -*- coding: utf-8 -*-

"""Module with methods to detect streaming info"""

import re

from resources.lib.misc import re_search
from resources.lib.misc import is_season

from resources.lib.log import log_msg


def crunchyroll_method(self, item):
    """Categorize Crunchyroll info.

    Args:
        item (json): JsonRPC content
    """
    # CRUNCHYROLL
    if 'crunchyroll' in item['file']:
        # CRUNCHYROLL SHOW DIRECTORY
        if item['filetype'] == 'directory':
            if re_search(item['file'], r'mode\=series'):
                if item['season'] == -1:
                    item['type'] = 'tvshow'
                    del item['episode']
                    del item['season']
            # CRUNCHYROLL SEASON DIRECTORY
            if re_search(item['file'], r'mode\=episodes'):
                item['type'] = 'season'
                if item['season'] == 0 or -1:
                    item['season'] = 1
                else:
                    item['season'] = int(
                        re.findall(
                            r'season\=(.+?)',
                            item['file'])[0]
                    )
                del item['episode']
        elif item['filetype'] == 'file':
            # CRUNCHYROLL EPISODE FILE
            if re_search(item['file'], r'mode\=videoplay'):
                item['episode'] = self.epindex
                item['type'] = 'episode'
                if item['season'] == 0 or -1:
                    item['season'] = 1
                else:
                    item['season'] = int(
                        re.findall(
                            r'season\=(.+?)',
                            item['file'])[0]
                    )
                # YEAR
                # TODO: Maybe year can be collected from file
                # with regex but aparently not all shows has year=XXXX info
                # maybe premiered=XXXX or aired=XXXX can work

def amazon_method(self, item):
    """Categorize Amazon info.

    Args:
        item (json): JsonRPC content
    """
    # AMAZON
    if 'amazon' in item['file']:
        if item['filetype'] == 'directory':
            # AMAZON SHOW DIRECTORY
            if item["episode"] == -1:
                if not is_season(item['label']) or item["type"] == "tvshow":
                    item['type'] = 'tvshow'
                    if item['label'] and not item['showtitle']:
                        item['showtitle'] = item['label']
                        self.showtitle = item['label']
                    else:
                        log_msg(
                            'AMAZON "label" is empty, showtitle will not be filled.'
                        )
                    del item['episode']
                    del item['season']
            # AMAZON SEASON DIRECTORY
            if is_season(item['label']):
                if item['season'] > -1:
                    item['type'] = 'season'
                    del item['episode']
                else:
                    # For now, categorize as trailher, ignore items like Extra / Trailer
                    item['type'] = 'trailer'
                    item['season'] = 1
        elif item['filetype'] == 'file':
            # AMAZON EPISODE FILE
            if item['episode'] > -1:
                if item['season'] > -1:
                    if item['type'] == 'episode':
                        item['showtitle'] = self.showtitle
                        item['episode'] = self.epindex
            else:
                # For now, categorize as trailher, ignore items like Extra / Trailer
                log_msg('Extra/Trailer ignored %s' % item)
                item['type'] = 'trailer'

def disney_method(_, item):
    """Categorize Disney Plus info.

    Args:
        item (json): JsonRPC content
    """
    # DISNEY
    if 'disney' in item['file']:
        # DISNEY SHOW DIRECTORY
        if item['filetype'] == 'directory':
            if item['type'] == 'tvshow':
                if not is_season(item['label']):
                    item['type'] = 'tvshow'
                    item['showtitle'] = item['title']
                    del item['episode']
                    del item['season']
            # DISNEY SEASON DIRECTORY
            if item['type'] == 'unknown':
                if is_season(item['label']):
                    item['type'] = 'season'
                    del item['episode']

def netflix_method(self, item):
    """Categorize Netflix info.

    Args:
        item (json): JsonRPC content
    """
    # NETFLIX
    if 'netflix' in item['file']:
        if item['filetype'] == 'directory':
            # NETFLIX SHOW DIRECTORY
            if re_search(item['type'], 'tvshow'):
                if not re_search(item['file'], ['season', 'episode']):
                    del item['episode']
                    del item['season']
            # NETFLIX SEASON DIRECTORY
            if item['type'] == 'unknown':
                if re_search(item['file'], ['show', 'season']):
                    if not re_search(item['file'], ['episode']):
                        if is_season(item['label']):
                            del item['episode']
                            item['type'] = 'season'
        elif item['filetype'] == 'file':
            # NETFLIX EPISODE FILE
            if item['type'] == 'episode':
                if re_search(item['file'], ['show', 'season', 'episode']):
                    if self.year is None:
                        if item['year'] > 1600:
                            self.year = item['year']

def hbomax_method(self, item):
    """Categorize HBO Max info.

    Args:
        item (json): JsonRPC content
    """
    # HBOMAX
    if 'slyguy.hbo.max' in item['file']:
        # HBOMAX SHOW DIRECTORY
        if item['filetype'] == 'directory':
            if re_search(item['type'], ['tvshow', 'unknown']):
                if item['season'] == -1:
                    if not is_season(item['label']):
                        item['showtitle'] = item['title']
                        item['type'] = 'tvshow'
                        del item['episode']
                        del item['season']
            # HBOMAX SEASON DIRECTORY
            if item['type'] == 'unknown':
                if is_season(item['label']):
                    del item['episode']
                    item['type'] = 'season'
                    item['season'] = self.epindex

def crackle_method(_, item):
    """Categorize Crackle info.

    Args:
        item (json): JsonRPC content
    """
    # CRACKLE
    if 'crackle' in item['file']:
        # CRACKLE SHOW DIRECTORY
        if item['filetype'] == 'directory':
            if item['type'] == 'tvshow':
                if item['season'] == -1:
                    if not is_season(item['label']):
                        item['showtitle'] = item['title']
                        item['type'] = 'tvshow'
                        del item['episode']
                        del item['season']

def paramountplus_method(_, item):
    """Categorize Paramount Plus info.

    Args:
        item (json): JsonRPC content
    """
    # PARAMOUNTPLUS
    if 'slyguy.paramount.plus' in item['file']:
        # PARAMOUNTPLUS SHOW DIRECTORY
        if item['filetype'] == 'directory':
            if re_search(item['type'], ['tvshow', 'unknown']):
                if item['season'] == -1:
                    if not is_season(item['label']):
                        item['showtitle'] = item['title']
                        item['type'] = 'tvshow'
                        del item['episode']
                        del item['season']
            # PARAMOUNTPLUS SEASON DIRECTORY
            if item['type'] == 'unknown':
                if is_season(item['label']):
                    del item['episode']
                    item['type'] = 'season'
                    item['season'] = item['number']


def raitv_method(_, item):
    """Categorize Raitv info.

    Args:
        item (json): JsonRPC content
    """
    # RAIPLAY
    if 'plugin.video.raitv' in item['file']:
        if item['filetype'] == 'directory':
            # RAIPLAY SHOW DIRECTORY
            if re_search(item['label'], 'Episodi'):
                item['type'] = 'tvshow'
                del item['episode']
                del item['season']
        elif item['filetype'] == 'file':
            # RAIPLAY EPISODE FILE
            item['type'] = 'episode'
            try:
                if item['episode'] == 0:
                    item['episode'] = item['number']
            except IndexError:
                pass
