# -*- coding: utf-8 -*-
import scrapy
import json
from bs4 import BeautifulSoup
from bs4.element import Comment
from monster.items import MonsterItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import SelectJmes,MapCompose,Join


#Using BeatifulSoup to escape the tags from the Description Field
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)




#Constructor of the Spider
class MonsterSpiderSpider(scrapy.Spider):
    name = 'monster-spider'
    allowed_domains = ['monster.com']
    
    def __init__(self,filename=None,*args,**kwargs):
        super(MonsterSpiderSpider, self).__init__(filename,*args, **kwargs)
        
        if filename:
            with open('urls.txt') as f:
               self.start_urls = [url.rstrip('\n') for url in f.readlines()]
               f.close()
               self.start_urls = [url + str(i) for i in range(1,25) for url in self.start_urls]
               print(self.start_urls)
    
  

#This function parses the webpage and scrapes the JobID of each job
#then adds the JobID to the next_url variable where the crawler redirects to the Job's JSON url-link
    def parse(self, response):
        results = json.loads(response.body)
        
        for i in range(len(results)):
            try:
                job_id = results[i]['MusangKingId']
                next_url = ('https://job-openings.monster.com/v2/job/pure-json-view?jobid={}').format(job_id) #Try to use a link to your browser to check all the available data
                                                                                                              #that can be scraped
                
                yield response.follow(next_url, callback =self.parse_detail)
            except:
                continue
        
   
#For each job-link the function pushes the scraped data to the ItemLoader function that add the values to the Item
    def parse_detail(self,response):

        

        result = json.loads(response.body)
        
        loader = ItemLoader(item = MonsterItem())
        
        loader.add_value('JobId',result['jobIdentification'])
        loader.add_value('Title',result['companyInfo']['companyHeader'])
        loader.add_value('Location',result['companyInfo']['jobLocation'])
        loader.add_value('Company',result['companyInfo']['name'])
        loader.add_value('Description',text_from_html(result["jobDescription"]))
        loader.add_value('Country',result['jobLocationCountry'])
       

            
        yield loader.load_item()
        
        
 