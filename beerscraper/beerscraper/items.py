# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BeerscraperItem(scrapy.Item):
    beer_url = scrapy.Field()
    brewery_url = scrapy.Field()
    style_url = scrapy.Field()
    rank = scrapy.Field()
    beer = scrapy.Field()
    brewery = scrapy.Field()
    style = scrapy.Field()
    abv = scrapy.Field()
    weighted_rank = scrapy.Field()
    reviews = scrapy.Field()
    hads = scrapy.Field()
    state = scrapy.Field()
    country = scrapy.Field()
