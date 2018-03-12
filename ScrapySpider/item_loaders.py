# -*- coding: utf-8 -*-
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


class FirstItemLoader(ItemLoader):
    """
    只取第一项的ItemLoader
    """
    default_output_processor = TakeFirst()
