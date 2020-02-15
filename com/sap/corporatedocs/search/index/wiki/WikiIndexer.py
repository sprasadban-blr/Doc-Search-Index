'''
regular expressions to try out
"[^ /(http|https|ftp|ftps)\:\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z0-9]]"
[^ a-zA-Z0-9]+/(http|https|ftp|ftps)\:\/\/[a-zA-Z0-9\-\.] 
'''
from elasticsearch import Elasticsearch
from com.sap.corporatedocs.search.index.common.MongoDB import MongoDB
import requests
import json
import re

class WikiIndexer(object):

    def __init__(self):
        self.eshost = "localhost"
        self.esport = 9200
        self.index = 'ngpbug-index'
        self.docType = 'ngpbug-docs'
        self.esurl = "http://" + self.eshost + ":" + str(self.esport)
        self.index = 'wiki-index'
        self.docType = 'wiki-docs'        
        self.link = ""
        self.title = ""
        self.lastModifiedDate = ""
        self.paragraph = ""
        self.outLinks = ""
        self.contents = ""
        self.mongodb = MongoDB()
        self.mongodb.connect()

    def _isElasticSearchRunning(self):
        isRunning = False
        res = requests.get(self.esurl)
        if(res.status_code == 200):        
            print(res.content)
            isRunning = True
        return isRunning
    
    def createWikiLinkInfoJSON(self):
        doc = {}
        doc['link'] = self.link
        doc['title'] = self.title
        doc['lastModifiedDate'] = self.lastModifiedDate
        doc['paragraph'] = self.paragraph
        doc['contents']=self.contents        
        doc['outLinks'] = self.outLinks
        return json.loads(json.dumps(doc))
    
    def indexWikiLinksInfo(self, flushIndex = False):
        if(not self._isElasticSearchRunning()):
            print("Start Elastic Search and then index contents\n")
            
        es = Elasticsearch([{'host': self.eshost, 'port': self.esport}])
        if(flushIndex):
            ''' First time flush throws 'index_not_found_exception'. Ignore the errors '''
            es.indices.delete(index=self.index, ignore=[400, 404])
                
        allWikiLinkInfo = self.mongodb.findAllWikiLinkInfo()
        indexPos = 1
        for aWikiLinkInfo in allWikiLinkInfo:            
            print(aWikiLinkInfo['link'])
            self.link = aWikiLinkInfo['link']
            self.title = aWikiLinkInfo['title']
            self.lastModifiedDate = aWikiLinkInfo['lastModifiedDate']
            ''' As is to index '''
            self.contents = aWikiLinkInfo['paragraph']
            ''' Remove special characters in paragraph '''
            self.paragraph = re.sub('[^ a-zA-Z0-9]', ' ', aWikiLinkInfo['paragraph'])
            ''' Remove unwanted spaces between words --> Split and Join words '''
            ''' This is for constructing valid JSON '''
            self.paragraph = " ".join(self.paragraph.split())
            self.outLinks = aWikiLinkInfo['outLinks']
            es.index(index=self.index, doc_type=self.docType, id=indexPos, body=self.createWikiLinkInfoJSON())
            indexPos = indexPos + 1 
        print("Total indexed Wiki docs = "+str(indexPos - 1))           
        
if __name__ == '__main__':
    wikiIndex = WikiIndexer()
    wikiIndex.indexWikiLinksInfo(True)      