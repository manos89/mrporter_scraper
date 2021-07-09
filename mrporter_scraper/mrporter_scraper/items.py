# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst


class MrporterScraperItem(scrapy.Item):
    # define the fields for your item here like:
    product_id = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    description = scrapy.Field(output_processor=TakeFirst())
    images = scrapy.Field()
    videos = scrapy.Field()
    category = scrapy.Field(output_processor=TakeFirst())
    additional_features = scrapy.Field()
    age_group = scrapy.Field(output_processor=TakeFirst())
    brand = scrapy.Field(output_processor=TakeFirst())
    capacity = scrapy.Field(output_processor=TakeFirst())
    color = scrapy.Field(output_processor=TakeFirst())
    SKU = scrapy.Field(output_processor=TakeFirst())
    attributes = scrapy.Field(output_processor=TakeFirst())
    UPC = scrapy.Field(output_processor=TakeFirst())
    full_price = scrapy.Field(output_processor=TakeFirst())
    price_with_discount = scrapy.Field(output_processor=TakeFirst())


class TextItem(scrapy.Item):
    # define the fields for your item here like:
    text = scrapy.Field(output_processor=TakeFirst())



