# -*- coding: utf-8 -*-

"""Module with class to with methods to detect streaming info."""

from resources.lib.log import log_msg
from resources.lib.misc import is_season, re_search, savetojson

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
        self.year = None
        self.epindex = None
        self.showtitle = None

    def loop(self, itens, sync_type, showtitle=False):
        """Loop function to get info from jsonRPC data."""
        savetojson(itens)
        try:
            if not self.year:
                self.year = min([x['year'] for x in itens if is_season(x['label'])])
                log_msg('----->>>>> %s ----> %s' % (self.year, itens))
        except ValueError:
            pass
        for index, item in enumerate(itens):
            self.epindex = index + 1
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
                    if is_season(item['label']):
                        if item['showtitle'] and not self.showtitle:
                            self.showtitle = item['showtitle']
                    if self.showtitle != item['showtitle'] and item['showtitle']:
                        self.showtitle = item['showtitle']
                        item['year'] = None
                    crunchyroll_method(self, item)
                    amazon_method(self, item)
                    disney_method(self, item)
                    netflix_method(self, item)
                    hbomax_method(self, item)
                    crackle_method(self, item)
                    paramountplus_method(self, item)
                    if self.year:
                        item['year'] = self.year
            except KeyError as error:
                log_msg("INFO DETETOR LOOP: %s, item: %s" % (error, item))
            yield item

    @staticmethod
    def movies_method(item):
        """Detect movies from all services."""
        del item['episode']
        del item['season']
        del item['showtitle']
