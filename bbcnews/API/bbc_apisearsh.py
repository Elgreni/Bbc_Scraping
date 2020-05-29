# -*- coding: utf-8 -*-
"""
Created on Sun May 17 16:36:15 2020

@author: laptech
"""

import json
from flask import Flask
from flask_restful import Resource, Api
from flask_pymongo import PyMongo
from bson import json_util

appli = Flask(__name__)
appli.config['MONGODB_URI'] = 'mongodb+srv://test:<test>@cluster0-wlb0d.mongodb.net/test?retryWrites=true&w=majority/BbcNewsDatabase'
appli.config['MONGODB_DB']= 'BbcNewsDatabase'

api = Api(appli)
mongo = PyMongo(appli)

def convertojson(data):
    return json.dumps(data, default=json_util.default)

class Newsmeta(Resource):
    def get(self):
        result = mongo.db.BbcCollection.find()
        json_results = []
        for res in result:
            json_results.append(res)
        return convertojson(json_results)
    


class Searchtextkeyword(Resource):
    
    def get(self, keyword):
        result = mongo.db.BbcCollection.find({'newstext': {'$regex': '.*' + keyword + '.*'}})
        json_results = []
        for res in result:
            json_results.append(res)
        return convertojson(json_results)    



class Searchnewstitlekeyword(Resource):
    def get(self, keyword):
        result = mongo.db.BbcCollection.find({'newstitl': {'$regex': '.*' + keyword + '.*'}})
        json_results = []
        for res in result:
            json_results.append(result)
        return convertojson(json_results)

appli.add_resource(Searchnewstitlekeyword,'/newstitl/<string:keyword>')
appli.add_resource(Searchtextkeyword, '/newstext/<string:keyword>')
appli.add_resource(Newsmeta, '/news')  

if __name__ =='__main__':
    appli.run



















