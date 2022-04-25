# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item,Field
from scrapy.loader.processors import TakeFirst,MapCompose


class MonsterItem(Item):
    JobId = Field(
        input_processor = MapCompose(),
        output_processor = TakeFirst()
             )

    Title = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
                 )

    Location = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
                )

    Company = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
                )

    Description = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
                )

    Country = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
                )
   

    
