# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NpmFantasticItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pkg_name = scrapy.Field()
    pkg_link = scrapy.Field()
    pkg_version = scrapy.Field()
    pkg_author = scrapy.Field()
    pkg_license = scrapy.Field()
    pkg_homepage = scrapy.Field()
    pkg_last_update = scrapy.Field()
    pkg_quality = scrapy.Field()
    pkg_collaborator = scrapy.Field()
    repo_link = scrapy.Field()
    repo_stars = scrapy.Field()

    pass
