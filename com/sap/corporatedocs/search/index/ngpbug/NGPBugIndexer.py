''' pip install elasticsearch '''
''' pip install requests '''
from elasticsearch import Elasticsearch
from com.sap.corporatedocs.search.index.common.MongoDB import MongoDB
import requests
import json
import re

class NGPBugIndexer(object):

    def __init__(self):
        self.eshost = "localhost"
        self.esport = 9200
        self.index = 'ngpbug-index'
        self.docType = 'ngpbug-docs'
        self.esurl = "http://" + self.eshost + ":" + str(self.esport)
        self.link = ""
        self.type = ""
        self.priority = ""
        self.component = ""
        self.status = ""
        self.contents = ""        
        self.description = ""
        self.comments = ""
        self.mongodb = MongoDB()
        self.mongodb.connect()
    
    def _isElasticSearchRunning(self):
        isRunning = False
        res = requests.get(self.esurl)
        if(res.status_code == 200):        
            print(res.content)
            isRunning = True
        return isRunning
    
    def _createNGPBugLinkInfoJSON(self):
        doc = {}
        doc['link'] = self.link
        doc['type'] = self.type
        doc['priority'] = self.priority
        doc['component'] = self.component
        doc['status'] = self.status
        doc['contents']=self.contents
        doc['description'] = self.description
        doc['comments'] = self.comments        
        return json.loads(json.dumps(doc))
    
    def _cleanUpText(self, aText):                        
        ''' Remove special characters in paragraph '''
        aCleanedText = re.sub('[^ a-zA-Z0-9]', ' ', aText)
        ''' remove unwanted spaces between words --> Split and Join words '''
        aCleanedText = " ".join(aCleanedText.split())
        return aCleanedText
    
    def _cleanUpAllText(self, aTextList):
        aFinalList = []
        if(aTextList is None):       
            return aFinalList
        for aText in aTextList:
            aFinalList.append(self._cleanUpText(aText))
        return aFinalList
        
    def indexNGPBugLinkInfo(self, flushIndex = False):
        if(not self._isElasticSearchRunning()):
            print("Start Elastic Search and then index contents\n")
            
        es = Elasticsearch([{'host': self.eshost, 'port': self.esport}])
        if(flushIndex):
            ''' First time flush throws 'index_not_found_exception'. Ignore the errors '''
            es.indices.delete(index=self.index, ignore=[400, 404])
                
        allNGPBugLinkInfo = self.mongodb.findAllNGPBugLinkInfo()
        indexPos = 1
        for aNGPBugLinkInfo in allNGPBugLinkInfo:            
            print(aNGPBugLinkInfo['link'])
            self.link = aNGPBugLinkInfo['link']            
            self.type = aNGPBugLinkInfo['type']
            self.priority = aNGPBugLinkInfo['priority']
            self.component = aNGPBugLinkInfo['component']
            self.status = aNGPBugLinkInfo['status']
            ''' As is to index '''
            self.contents = aNGPBugLinkInfo['description']
            self.description = self._cleanUpText(aNGPBugLinkInfo['description'])
            self.comments = self._cleanUpAllText(aNGPBugLinkInfo['comments'])
            es.index(index=self.index, doc_type=self.docType, id=indexPos, body=self._createNGPBugLinkInfoJSON())
            indexPos = indexPos + 1 
        print("Total indexed NGPBug docs = "+str(indexPos - 1))           

if __name__ == '__main__':
    indexer = NGPBugIndexer()
    indexer.indexNGPBugLinkInfo(True)
            