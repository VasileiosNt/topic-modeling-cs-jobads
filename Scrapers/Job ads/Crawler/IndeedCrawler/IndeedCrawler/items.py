from scrapy.item import Item,Field
from scrapy.loader.processors import MapCompose, TakeFirst


def remove_quotes(text):
    # strip the unicode quotes
    text = text.strip(u'\u201c'u'\u201d')
    return text

class IndeedItem(Item):

    JobId = Field(
        input_processor = MapCompose(),
        output_processor = TakeFirst()
    )
    JobTitle = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    Company = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    Location = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    Rating = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    Description = Field(
         input_processor = MapCompose(),
        output_processor = TakeFirst()
    )
    
    Country = Field(
         input_processor = MapCompose(),
         output_processor = TakeFirst()
    )
   
