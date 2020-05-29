# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from   scrapy.exceptions import DropItem
from   scrapy import signals
from   pydispatch import dispatcher
from   scrapy.exporters import JsonItemExporter
from readability import Document
from   scrapy.conf import settings
import requests, html2text
import pymongo, logging
from   datetime import datetime





class BbcnewsPipeline:
    def process_item(self, item, spider):
        return item


class Textpipeline_news(object):
    
    def process(self, item, spider):
        try:
            response = requests.get(item['newsurl'])
            doc = Document(response.text)
            content = Document(doc.content()).summary()
            h = html2text.HTML2Text()
            h.ignore_links = True
            articltext = h.handele(content)
            articltext = articltext.replace('\r', ' ').replace('\n', ' ').strip()
            item['newstext'] = articltext
            
        except Exception:
            raise DropItem("extract article Failed from: " + item['newsurl'])
        return item
    
            
class Emptypipelinedrop(object):
    
    def item_process(self, item, spider):
        if ((not item['newstitl']) or (not item['newsurl']) or (not item['newsauthor']) or (not item['newstext'])):
            raise DropItem()
        else:
            return item
        

class PipelineDuplicated(object):
    
    def __init__(self):
        self.ids_seen = set()
        
    def process_item(self, item, spider):
        if item['newsurl'] in self.ids_seen:
            raise DropItem("Duplicate Found: %s" % item)
        else:
            self.ids_seen.add(item['newsurl'])
            return item


class Mongodbpipeline(object):
    
    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_URI'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
        
    def process_item(self, item, spider):
        valid = True
        for data in item:
            if((data == 'newsurl' or data == 'newstitl' or data == 'newsauthor' or data == 'newstext') and not data):
                valid = False
                raise DropItem('News item dropped.missing' + data)
            if valid:
                self.collection.insert(dict(item))
                logging.info('news inserted in database (Mongodb)')
            return item



class ExportjsonPipeline(object):
    
    def __init__(self):
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.fjsons = {}
        
        
    def spider_opened(self, spider):
        fjson = open('Output/newsbbc_'+ datetime.now().strftime("%Y%m%d%H%M%S") + '.json', 'wb')    
        self.fjson[spider] = fjson
        self.exported = JsonItemExporter(fjson)
        self.exported.start_exporting()
        
        
    def spider_closed(self, spider):
        self.exported.finish_exporting()
        fjson = self.fjson.pop(spider)
        fjson.close()
        
        
        
    def process_item(self, item, spider):
        self.exported.export_item(item)
        return item
        
        
        
       
          
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            