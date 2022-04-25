import scrapy
from scrapy.loader import ItemLoader
from IndeedCrawler.items import IndeedItem



class IndeedSpider(scrapy.Spider):
    #Handle the redirects
    handle_httpstatus_list = [301,302]
    allowed_domains = ['indeed.ch','at.indeed.com','de.indeed.com']
    name = "indeed-spider"
    
    def __init__(self,filename=None):
        if filename:
            with open('urls.txt') as f:
                self.start_urls = [url.rstrip() for url in f.readlines()]
                self.start_urls = [url + str(i*10) for i in range(0,25) for url in self.start_urls] 
                

		
    
    def parse (self,response):

        if response.request.url.startswith('https://at'):
            Country = 'Austria'

        elif response.request.url.startswith('https://de'):
            Country = 'Germany'
        else:
            Country = 'Switzerland'

        #css selector to fetch the job dib
        result = response.css('div.jobsearch-SerpJobCard')

        for job in result:

            loader  = ItemLoader(item = IndeedItem(),selector=job)
            #Scraping the rating from the home page | Assing "Not found" if its not there
            rating = job.css('.sjcl .ratingsDisplay .ratingNumber .ratingsContent::text').get()
            if rating is None:
                rating = 'Not Available'
            loader.add_value('Rating',rating)
            loader.add_value('Country',Country)
            #Get the key of the job
            job_id = job.css('div.title a:nth-child(1)::attr(id)').get()
          
            #Load the key and push it to meta with the rating
            loader.add_value('JobId',job_id)
            job_item=loader.load_item()
            

            #Get the url's of each job,slice the first 3 characters
            next_url = ('https://www.indeed.ch/Zeige-Job?jk={}').format(job_id[3:])
 
                    
            yield response.follow(next_url,callback=self.parse_job,meta={'job_item':job_item})
            
    

    def parse_job(self,response):
        #css selector of the jobLayout
        result = response.css('div.jobsearch-ViewJobLayout-innerContentGrid')

        for data in result:
            #Load the previous items{rating,jobID} from the previous function
            job_item = response.meta['job_item']
            #Initialize Itemloader
            loader  = ItemLoader(item = job_item,selector=data)
            
            #add Title
            loader.add_css('JobTitle','h3.jobsearch-JobInfoHeader-title::text')

            #add Company
            company_name = data.css('div.icl-u-xs-mr--xs a::text').get()
            if company_name is None:
                company_name = data.css('div.icl-u-xs-mr--xs::text').get()
            loader.add_value('Company',company_name)

             #addLocation   
            loader.add_css('Location','span.jobsearch-JobMetadataHeader-iconLabel::text')
            #addDescription
            loader.add_xpath('Description','normalize-space(.//div[@id="jobDescriptionText"])')
            
            #Return item 
            yield loader.load_item()
            

    
    
    # for job in result:
    #         loader  = ItemLoader(item = IndeedItem(),selector=job)

    #         loader.add_xpath('Title','normalize-space(.//div[@class="title"])')

    #         #Companies are missing <a>
    #         company_name = job.xpath('.//div[@class="sjcl"]/div/span[@class="company"]/a/text()').get() 
    #         if company_name is None:
    #             company_name = job.xpath('.//div[@class="sjcl"]/div/span[@class="company"]/text()').get()
    #         loader.add_value('Company',company_name)

    #         loader.add_css('Location','.location::text ')

    #         #Ratings are missing
    #         rating = job.css('.sjcl .ratingsDisplay .ratingNumber .ratingsContent::text').get()
    #         if rating is None:
    #             rating = 'Not Available'
    #         loader.add_value('Rating',rating)
        

            
        
