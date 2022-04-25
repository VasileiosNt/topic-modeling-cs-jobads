from scrapy.item import Item,Field
from scrapy.loader.processors import MapCompose, TakeFirst
import scrapy



class StepstoneJob(scrapy.Item):
    JobTitle = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    Company = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    Description = Field(
         input_processor = MapCompose(),
        output_processor = TakeFirst()
    )

    Location = Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    JobId  = Field(

        input_processor = MapCompose(),
        output_processor = TakeFirst()
    )
    Country = Field(

        input_processor = MapCompose(),
        output_processor = TakeFirst()
    )