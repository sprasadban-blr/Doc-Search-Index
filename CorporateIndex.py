''' pip install flask flask-restful '''
''' REST Sample: https://www.codementor.io/sagaragarwal94/building-a-basic-restful-api-in-python-58k02xsiq '''
''' Elastic search by multi fields: https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-multi-match-query.html '''
''' Get all elastic search results: https://stackoverflow.com/questions/8829468/elasticsearch-query-to-return-all-records '''

from flask import Flask
from flask_restful import Resource, Api
from elasticsearch import Elasticsearch
import json
import timeit

class WikiIndex(Resource):
    def __init__(self):
        self.eshost = "localhost"
        self.esport = 9200
        self.index = 'wiki-index'
        self.docType = 'wiki-docs'        
        self.es = Elasticsearch([{'host': self.eshost, 'port': self.esport}])

    def get(self, pattern):
        ''' Try by Link ID '''
        requestedItemsPerPage = 5000
        start = timeit.default_timer()
        docs = self._getBestFieldsDocs(pattern, requestedItemsPerPage)
        stop = timeit.default_timer()
        total = docs['hits']['total']
        print("Total=", total)
        result = self._processResult(docs, total, round((stop - start), 2), requestedItemsPerPage)
        return json.loads(json.dumps(result))        
            
    def _getMostFieldsDocs(self, pattern, requestedItemsPerPage):
        param = {}
        param['scroll']='2m'
        param['size']=requestedItemsPerPage
        docs = self.es.search(index=self.index, doc_type=self.docType, 
                              body={"query": {"multi_match" : {"query": pattern, "type":  "most_fields", "fields": ["link", "title", "contents"]}}},
                              params=param)
        return docs 
    
    def _getBestFieldsDocs(self, pattern, requestedItemsPerPage):
        param = {}
        param['scroll']='2m'
        param['size']=requestedItemsPerPage        
        docs = self.es.search(index=self.index, doc_type=self.docType,
                              body={"query": {"multi_match" : {"query": pattern, "type": "best_fields", "fields": ["link", "title", "contents"], "tie_breaker": 0.3}}},
                              params=param)
        return docs        
    
    def _getPhraseFieldsDocs(self, pattern, requestedItemsPerPage):
        param = {}
        param['scroll']='2m'
        param['size']=requestedItemsPerPage        
        docs = self.es.search(index=self.index, doc_type=self.docType,
                              body={"query": {"multi_match" : {"query": pattern, "type": "phrase_prefix", "fields": ["link", "title", "contents"]}}},
                              params=param)
        return docs 
                   
    def _processResult(self, docs, total, timeTaken, requestedItemsPerPage):
        visitedLinks = []
        allData = {}
        result = []
        allData['total'] = total 
        allData['timeTaken'] = timeTaken
        
        sid = docs['_scroll_id']
        scroll_size = docs['hits']['total']
        
        ''' All results are in first cursor '''
        if(scroll_size <= requestedItemsPerPage):
            result = self._getResults(docs['hits']['hits'], visitedLinks)
        else:
            while (scroll_size > 0):
                page = self.es.scroll(scroll_id = sid, scroll = '2m')
                # Update the scroll ID
                sid = page['_scroll_id']
                ''' Page wise get data '''
                hits = page['hits']['hits']
                result = self._appendList(result, self._getResults(page['hits']['hits'], visitedLinks))
                # Get the number of results that we returned in the last scroll
                scroll_size = len(hits)
                        
        allData['result'] = result
        return allData
    
    def _getResults(self, hits, visitedLinks):
        result = []
        for hit in hits:
            ''' Remove duplicate links '''
            if(hit['_source']['link'] not in visitedLinks):
                visitedLinks.append(hit['_source']['link'])
                data = {}
                data['link'] = hit['_source']['link']
                data['title'] = hit['_source']['title']
                ''' Valid for JSON construction '''
                data['paragraph'] = hit['_source']['paragraph']            
                result.append(data)
        return result

    def _appendList(self, source, target):
        for item in target:
            source.append(item)
        return source
        
    
class NGPBugIndex(Resource):
    def __init__(self):    
        self.eshost = "localhost"
        self.esport = 9200
        self.index = 'ngpbug-index'
        self.docType = 'ngpbug-docs'        
        self.es = Elasticsearch([{'host': self.eshost, 'port': self.esport}])
    
    def get(self, pattern):
        ''' Try by Link ID '''
        requestedItemsPerPage = 5000        
        start = timeit.default_timer()
        docs = self._getBestFieldsDocs(pattern, requestedItemsPerPage)
        stop = timeit.default_timer()
        total = docs['hits']['total']
        print("Total=", total)
        result = self._processResult(docs, total, round((stop - start), 2), requestedItemsPerPage)
        return json.loads(json.dumps(result))        
    
    
    def _getMostFieldsDocs(self, pattern, requestedItemsPerPage):
        param = {}
        param['scroll']='2m'
        param['size']=requestedItemsPerPage        
        docs = self.es.search(index=self.index, doc_type=self.docType, 
                              body={"query": {"multi_match" : {"query": pattern, "type":  "most_fields", "fields": ["link", "component", "contents"]}}},
                              params=param)
        return docs 
    
    def _getBestFieldsDocs(self, pattern, requestedItemsPerPage):
        param = {}
        param['scroll']='2m'
        param['size']=requestedItemsPerPage        
        docs = self.es.search(index=self.index, doc_type=self.docType, 
                              body={"query": {"multi_match" : {"query": pattern, "type": "best_fields", "fields": ["link", "component", "contents"], "tie_breaker": 0.3}}},
                              params=param)
        return docs        
    
    def _getPhraseFieldsDocs(self, pattern, requestedItemsPerPage):
        param = {}
        param['scroll']='2m'
        param['size']=requestedItemsPerPage        
        docs = self.es.search(index=self.index, doc_type=self.docType, 
                              body={"query": {"multi_match" : {"query": pattern, "type": "phrase_prefix", "fields": ["link", "component", "contents"]}}},
                              params=param)
        return docs 
                   
    def _processResult(self, docs, total, timeTaken, requestedItemsPerPage):
        visitedLinks = []
        allData = {}
        result = []
        allData['total'] = total 
        allData['timeTaken'] = timeTaken
        
        sid = docs['_scroll_id']
        scroll_size = docs['hits']['total']
        
        ''' All results are in first cursor '''
        if(scroll_size <= requestedItemsPerPage):
            result = self._getResults(docs['hits']['hits'], visitedLinks)
        else:
            while (scroll_size > 0):
                page = self.es.scroll(scroll_id = sid, scroll = '2m')
                # Update the scroll ID
                sid = page['_scroll_id']
                ''' Page wise get data '''
                hits = page['hits']['hits']
                result = self._appendList(result, self._getResults(page['hits']['hits'], visitedLinks))
                # Get the number of results that we returned in the last scroll
                scroll_size = len(hits)
                        
        allData['result'] = result
        return allData
    
    def _getResults(self, hits, visitedLinks):
        result = []
        for hit in hits:
            ''' Remove duplicate links '''
            if(hit['_source']['link'] not in visitedLinks):
                visitedLinks.append(hit['_source']['link'])
                data = {}
                data['link'] = hit['_source']['link']
                data['component'] = hit['_source']['component']
                ''' Valid for JSON construction '''
                data['description'] = hit['_source']['description']            
                result.append(data)
        return result
    
    def _appendList(self, source, target):
        for item in target:
            source.append(item)
        return source
        
class CorporateIndex(object):
    def __init__(self):
        self.indexdata = ""
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(WikiIndex, '/wiki/<pattern>')
        self.api.add_resource(NGPBugIndex, '/ngpbug/<pattern>')
        self.startIndexApp()
        
    def startIndexApp(self):
        self.app.run(host="10.53.216.88", port=5002)
        #self.app.run(port=5002)
            
if __name__ == '__main__':
    index = CorporateIndex()
