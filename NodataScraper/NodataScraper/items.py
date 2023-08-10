# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NodataPageItem(scrapy.Item):
    artist_album_and_year = scrapy.Field()
    published_date = scrapy.Field()
    tags = scrapy.Field()
    image_urls = scrapy.Field()
    # images = scrapy.Field()
    label = scrapy.Field()
    comment_number = scrapy.Field()
    album_url = scrapy.Field()


class NodataDBItem(scrapy.Item):
    artist = scrapy.Field()
    album = scrapy.Field()
    album_creation_year = scrapy.Field()
    published_date = scrapy.Field()
    tags = scrapy.Field()
    image_urls = scrapy.Field()
    # images = scrapy.Field()
    label = scrapy.Field()
    comment_number = scrapy.Field()
    album_url = scrapy.Field()

