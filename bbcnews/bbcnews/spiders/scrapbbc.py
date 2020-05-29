# -*- coding: utf-8 -*-


import scrapy
from bbcnews.items import BbcnewsItem  
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import os, logging, json
  
#from austmps.items import AustmpsItem

class BbcNewsSpider(CrawlSpider):
    name ='bbcdata'
    rules =[]
    
    def Crawlingrule(self):
        for rule in self.rulefile["rules"]:
            allow_r = ()
            if 'allow' in rule.keys():
                allow_r = [al for al in rule['allow']]
                
            deny_r = ()
            if 'deny' in rule.keys():
                deny_r = [dy for dy in rule['deny']]


            restrict_xpath_r = ()
            if 'restrict_xpath' in rule.keys():
               restrict_xpath_r = [rpath for rpath in rule['restrict_xpath_r']]
            
            BbcNewsSpider.rules.append(Rule(LinkExtractor(allow=allow_r, deny=deny_r, restrict_xpath=restrict_xpath_r),follow=rule['follow'],callback=rule['callback']))

    def urlvisitread(self):
        v_urlfile = 'Out/urlVisit.txt'
        try:
            fil_url = open(v_urlfile, 'r')
        except IOError:
            self.urls_visit = []
        else:
            self.urls_visit = [url.strip() for url in fil_url.readline()]
            fil_url.close()
        finally:
            if not os.path.exists('Output/'):
                os.makedirs('Output/')
            self.urlfile = open(v_urlfile, 'a')

    
    
    def __init__(self):
        self.ruleFile = json.load(open('bbcnewRules.json'))
        self.allows_domains = self.ruleFile['allows_domains']
        self.start_urls = self.ruleFile['start_urls']
        
        self.Crawlingrule()
        self.urlvisitread()
        super(BbcNewsSpider,self).__init__()
        
        
    def getauthor(self,hxs):
        author = hxs.xpath(self.ruleFile['paths']['author'][0].extract())
        if not author :
            author = hxs.xpath(self.ruleFile['paths']['author'][1].extract())
            
        if author :
            return author[0].encode('ascii', 'ignore')
        else :
            return ''
        
        
      
        
    def itemPars(self, response):
        if str(response.url) not in self.urls_visit:
            try:
                logging.info('URL Parse: ' + str(response.url))
                news = BbcnewsItem()
                hxs = scrapy.Selector(response)
                
                news['newsurl'] = response.url
                
                titl = hxs.xpath(self.ruleFile['paths']['title'][0]).extract()[0]
                if titl:
                    news['newsHeadline'] = titl.encode('ascii', 'ignore')
                
                news['author'] = self.getauthor(hxs)    
                
                self.urlfile.write(str(response.url) + '/n')
                yield news
                
            except Exception :
                pass
            
            
            
    def close(spider, reason):
         spider.urlfile.close()
         
            
    
        
          










    
#class BbcNewsSpider(scrapy.Spider):
 #   name = 'bbcdata'
 #   allowed_domains = ['www.bbc.com']
 #   start_urls = ['https://www.bbc.com/news/']
    
 #   def parse(self, response):
        
        
  #      for resource in response.xpath("//div[@class='gs-c-promo-body gel-1/2@xs gel-1/1@m gs-u-mt@m']"):
   #         item = BbcnewsItem()
            
           # item = AustmpsItem()
            
    #        item['newstitl'] = response.xpath(".//div/a[@class='gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor']/h3/text()").extract_first()
     #       item['newsurl'] = response.xpath(".//div/a[@class='gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor']/a/@href").extract_first()
            
            #for resource in response.xpath(".//div/a[@class='gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor']/@href").extract_first():
            #    item['newsauthor'] = response.xpath(".//div[@class='byline']/span[@class='byline__name']/text()").extract_first()
             #   item['newstext'] = response.xpath(".//div[@class='story-body']/div[@class='story-body__inner']/p/text()").extract_first()
      #      return
        
            #print(item['newstitl'],item['newsurl'])
            
                 
        #pg_next = response.xpath("//div/a[@class='gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor']/@href")
            
            
        #if pg_next is not None:
            #path =  pg_next.extract_first()
            #pg_nextlink = response.urljoin(path)
            
            
            #print("found Url: {}".format(pg_nextlink))
            
            #yield scrapy.Request(url=pg_nextlink, callback=self.parse)
           # for resource in pg_nextlink:
                #author = response.xpath(".//div[@class='byline']/span[@class='byline__name']/text()").extract()
                #ar_text = response.xpath(".//div[@class='story-body']/div[@class='story-body__inner']/p/text()").extract()
                    
            
           
    