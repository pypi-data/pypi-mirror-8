# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup

from metro.parser.base import BaseRuDataProvider


class DataProvider(BaseRuDataProvider):
    metro_data_src = u"http://ru.wikipedia.org/wiki/\
                       Список_станций_Казанского_метрополитена"

    def download_all(self):
        self.parse_usual_big_table()
