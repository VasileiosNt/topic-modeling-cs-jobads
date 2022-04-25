import scrapy
from scrapy.loader import ItemLoader
from StepstoneCrawler.items import StepstoneJob
import hashlib
import re


class StepstoneSpider(scrapy.Spider):

    allowed_domains = ["stepstone.at", "stepstone.de"]
    handle_httpstatus_list = [301, 302]
    name = "stepstone-spider"

    def __init__(self, filename=None):
        if filename:
            with open("urls.txt") as f:
                self.start_urls = [url.strip() for url in f.readlines()]
                # substr='of='
                # self.start_urls = [re.sub(substr,substr+str(i*25),url) for i in range(0,25) for url in self.start_urls]

    def parse(self, response):

        if response.request.url.startswith("https://www.stepstone.at"):
            location = "at"
            Country = "Austria"
        else:
            location = "de"
            Country = "Germany"

        result = response.css("div.pagelayout")
        for job in result:

            try:
                loader = ItemLoader(item=StepstoneJob(), selector=job)
                loader.add_value("Country", Country)
                job_url = job.css(
                    "div.JobItemFirstLineWrapper-sc-11l5pt9-2 a::attr(href)"
                ).extract_first()
                next_url = "https://www.stepstone." + location + "/" + job_url
                hash_url = hashlib.md5(next_url.encode())
                Job_Id = hash_url.hexdigest()
                loader.add_value("JobId", Job_Id)
                job_id_item = loader.load_item()
            except:
                "Error"
            yield response.follow(
                next_url, callback=self.parse_job, meta={"job_item": job_id_item}
            )

    def parse_job(self, response):

        job_id_item = response.meta["job_item"]

        loader = ItemLoader(item=job_id_item, response=response)
        loader.add_css("JobTitle", "h1.at-header-company-jobTitle::text")
        loader.add_css("Company", "a.at-header-company-name::text")
        loader.add_value("Location", "Not Found")
        loader.add_xpath(
            "Description", 'normalize-space(.//div[@class="js-app-ld-ContentBlock"])'
        )

        yield loader.load_item()
