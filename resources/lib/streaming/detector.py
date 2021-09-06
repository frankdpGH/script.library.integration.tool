# -*- coding: utf-8 -*-

"""Module with class to with methods to detect streaming info."""

from resources.lib.log import log_msg
from resources.lib.misc import re_search, savetojson

from resources.lib.streaming.services import crunchyroll_method
from resources.lib.streaming.services import amazon_method
from resources.lib.streaming.services import disney_method
from resources.lib.streaming.services import netflix_method
from resources.lib.streaming.services import hbomax_method
from resources.lib.streaming.services import crackle_method
from resources.lib.streaming.services import paramountplus_method


class StreamingInfoDetector():
    """StreamingInfoDetector class to detect/categorize streaming info."""

    def __init__(self):
        self.year = 0
        self.epindex = None
        self.showtitle = None

    def loop(self, itens, sync_type, showtitle=False):
        """Loop function to get info from jsonRPC data."""
        self.showtitle = showtitle
        for index, item in enumerate(itens):
            self.epindex = index + 1
            if not self.showtitle:
                if item['showtitle']:
                    self.showtitle = item['showtitle']
            if self.year == 0:
                self.year = item['year']
            elif item['year'] < self.year != 0:
                self.year = item['year']
            # TODO: check if logic is real necessary, test is for all languages eficient
            if sync_type != 'all_items':
                if sync_type == 'movie' and item['type'] == 'movie':
                    pass
                elif sync_type == 'tvshow':
                    tvshow_search = [
                        'tvshow',
                        'season',
                        'episode',
                        'unknown',
                        'directory'
                    ]
                    if re_search(item['type'], tvshow_search):
                        pass
                elif sync_type == 'music' and item['type'] == 'music':
                    pass
                else:
                    continue
            try:
                if item['filetype'] == 'file' and item['type'] == 'movie':
                    self.movies_method(item)
                else:
                    if '' != item['showtitle'] != self.showtitle:
                        # updates self.showtitle when item['showtitle']
                        # changes and is not empty
                        self.showtitle = item['showtitle']
                        # reset self.year if item['showtitle'] is changed
                        self.year = 0
                    crunchyroll_method(self, item)
                    amazon_method(self, item)
                    disney_method(self, item)
                    netflix_method(self, item)
                    hbomax_method(self, item)
                    crackle_method(self, item)
                    paramountplus_method(self, item)
                    if not item['showtitle']:
                        item['showtitle'] = self.showtitle
            except KeyError:
                pass
            if item['year'] == 1601:
                item['year'] = 0
            if item['year'] > self.year and item['year'] != 0:
                item['year'] = self.year
            yield item

    @staticmethod
    def movies_method(item):
        """Detect movies from all services."""
        del item['episode']
        del item['season']
        del item['showtitle']
