# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PictureItem(scrapy.Item):
    title = scrapy.Field()
    img_s = scrapy.Field()
    image_paths = scrapy.Field()
