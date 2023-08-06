# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from django.utils.translation import get_language


class BaseDataProvider(object):
    """ Basic data provider
    with base methods, helpers and universal parsers
    """
    # base models
    line_model = None
    station_model = None
    # various parser stuff
    bg_word = 'background:'
    without_brackets_re = re.compile(ur'\s*\(.*\)')
    lang = None

    """ main methods
    """
    def __init__(self, station_model=None, line_model=None):
        if station_model and line_model:
            self.station_model = station_model
            self.line_model = line_model
            self.lang = get_language()
        else:
            raise AttributeError(
                u'You need to provide base station and line models'
            )

    def download_all(self):
        self.download_lines()
        self.download_stations()

    def download_lines(self):
        pass

    def download_stations(self):
        pass

    """ helper methods
    """
    def create_dom(self, url):
        get = lambda: BeautifulSoup(requests.get(url).content)
        try:
            html = get()
        except:
            # one more try
            try:
                html = get()
            except:
                return None
        return html

    def get_or_create_line(self, i, el_or_title, color=None):
        is_tag = isinstance(el_or_title, Tag)
        line, _ = self.line_model.objects.get_or_create(
            **dict(
                number=i,
                defaults=dict(
                    title=self.prep_title(el_or_title),
                    color=self.prep_color(el_or_title if is_tag else color),
                )
            )
        )
        return line

    def get_or_create_station(self, line, el):
        station, _ = self.station_model.objects.get_or_create(
            line=line,
            title=self.prep_title(self.get_el_text(el)),
        )
        return station

    def get_el_text(self, el):
        return el.get_text() if isinstance(el, Tag) else unicode(el)

    def prep_color(self, el):
        try:
            element = el['style'] if isinstance(el, Tag) else el
            return element\
                .replace(self.bg_word, '')\
                .replace(';', '')\
                .strip()
        except KeyError:
            return ''


class BaseRuDataProvider(BaseDataProvider):
    """ Basic data provider for ru lang
    """
    line_word = u'линия'
    clean_title_re = re.compile(ur'[^а-яА-ЯёЁa-zA-Z0-9\s\.,-_]*', re.U | re.I)

    def prep_title(self, el):
        return self.translit_if_needed(
            self.clean_title_re.sub(
                '',
                self.without_brackets_re.sub(
                    '',
                    self.get_el_text(el)\
                        .replace(self.line_word, '')\
                        .strip()
                )
            )
        )

    def translit_if_needed(self, el):
        if 'ru' not in self.lang:
            return self.transliterate(el)
        return el

    def transliterate(self, s):
        # reduce requirements
        repl_dict = {
            # upper
            u'А': u'A', u'Б': u'B', u'В': u'V', u'Г': u'G', u'Д': u'D',
            u'Е': u'E', u'Ё': u'Yo', u'З': u'Z', u'И': u'I', u'Й': u'Y',
            u'К': u'K', u'Л': u'L', u'М': u'M', u'Н': u'N', u'О': u'O',
            u'П': u'P', u'Р': u'R', u'С': u'S', u'Т': u'T', u'У': u'U',
            u'Ф': u'F', u'Х': u'H', u'Ъ': u'', u'Ы': u'Y', u'Ь': u'',
            u'Э': u'E', u'Ж': u'Zh',  u'Ц': u'Ts', u'Ч': u'Ch', u'Ш': u'Sh',
            u'Щ': u'Sch', u'Ю': u'Yu', u'Я': u'Ya',
            # lower
            u'а': u'a', u'б': u'b', u'в': u'v', u'г': u'g',
            u'д': u'd', u'е': u'e', u'ё': u'yo', u'ж': u'zh', u'з': u'z',
            u'и': u'i', u'й': u'y', u'к': u'k', u'л': u'l', u'м': u'm',
            u'н': u'n', u'о': u'o', u'п': u'p', u'р': u'r', u'с': u's',
            u'т': u't', u'у': u'u', u'ф': u'f', u'х': u'h', u'ц': u'ts',
            u'ч': u'ch', u'ш': u'sh', u'щ': u'sch', u'ъ': u'', u'ы': u'y',
            u'ь': u'', u'э': u'e', u'ю': u'yu', u'я': u'ya',
        }
        for key in repl_dict:
            s = s.replace(key, repl_dict[key])
        return s

    """ universal cases
    """
    # case with one big table, containing all lines and stations
    def parse_usual_big_table(self, station_td_count=None, table_number=None):
        i = 0
        line = None
        html = self.create_dom(self.metro_data_src)
        # search only in body
        body = html.find(id='mw-content-text')
        if table_number:
            table = body.find_all('table')[table_number]
        else:
            table = body.find('table')
        # get tbody instead of table, if exist
        tbody = table.find('tbody', recursive=False)
        if tbody:
            table = tbody
        stations = []
        for tr in table.find_all('tr', recursive=False):
            td = tr.find('td', recursive=False)
            if td:
                if 'rowspan' in td.attrs:
                    continue
                if self.line_word in td.get_text():
                    i += 1
                    line = self.get_or_create_line(i, td)
                elif line:
                    if 'colspan' in td.attrs:
                        break
                    # additional check for some cases
                    if station_td_count:
                        count = len(
                            tr.find_all('td', recursive=False)
                        )
                        if count != station_td_count:
                            continue
                    self.get_or_create_station(line, td)


class BaseEnDataProvider(BaseDataProvider):
    """ Basic data provider for en lang
    """
    base_en_url = u'http://en.wikipedia.org'
    without_sbrackets_re = re.compile(ur'\s*\[.*\]')

    def prep_title(self, el):
        return self.without_brackets_re.sub(
            '', self.without_sbrackets_re.sub(
                '', self.get_el_text(el).strip()
            )
        )
