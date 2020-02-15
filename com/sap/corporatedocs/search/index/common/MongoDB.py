''' pip install pymongo '''

from pymongo import MongoClient

class MongoDB(object):
    def __init__(self):
        self.client = ""
        self.db = ""

    def connect(self, server='localhost', port=27017):
        self.client = MongoClient(server, port)
        self.corpdocsDB = self.client.corporatedocs
        
    '''Gather wiki link and its html pages'''        
    def _getWikiDataCollection(self):
        return self.corpdocsDB.wiki_data
    
    def insertWikiData(self, wikiDoc):
        return self._getWikiDataCollection().insert_one(wikiDoc)
    
    def findAllWikiLinks(self):
        return self._getWikiDataCollection().find()
    
    def removeWikiData(self):
        self._getWikiDataCollection().remove()
        
    '''Gather wiki links and its important information'''                
    def _getWikiLinkInfoCollection(self):
        return self.corpdocsDB.wiki_link_info
    
    def insertWikiLinkInfo(self, wikiLinkInfo):
        return self._getWikiLinkInfoCollection().insert_one(wikiLinkInfo)
    
    def removeWikiLinkInfo(self):
        self._getWikiLinkInfoCollection().remove()
    
    def findAllWikiLinkInfo(self):
        return self._getWikiLinkInfoCollection().find()

    '''Gather all NGP Bug links'''            
    def _getNGPBugLinksCollection(self):
        return self.corpdocsDB.ngpbug_links
    
    def insertNGPBugLink(self, ngpbugLinkDoc):
        return self._getNGPBugLinksCollection().insert_one(ngpbugLinkDoc)

    def removeNGPBugLink(self):
        self._getNGPBugLinksCollection().remove()
    
    def findAllNGPBugLinks(self):
        return self._getNGPBugLinksCollection().find()
    
    '''Gather NGP Bug links and its html pages'''            
    def _getNGPBugDataCollection(self):
        return self.corpdocsDB.ngpbug_data
    
    def insertNGPBugData(self, ngpbugDoc):
        return self._getNGPBugDataCollection().insert_one(ngpbugDoc)

    def removeNGPBugData(self):
        self._getNGPBugDataCollection().remove()
    
    def findAllNGPBugData(self):
        return self._getNGPBugDataCollection().find()

    def findAllProcessedNGPBugData(self):
        return self._getNGPBugDataCollection().find({}, {"link":1})
    
    '''Gather relevant NGP Bug link info '''            
    def _getNGPBugLinkInfoCollection(self):
        return self.corpdocsDB.ngpbug_link_info
    
    def insertNGPBugLinkInfo(self, ngpbugLinkInfoDoc):
        return self._getNGPBugLinkInfoCollection().insert_one(ngpbugLinkInfoDoc)
    
    def removeNGPBugLinkInfo(self):
        self._getNGPBugLinkInfoCollection().remove()    
    
    def findAllNGPBugLinkInfo(self):
        return self._getNGPBugLinkInfoCollection().find()

    '''Gather user inputs from recast'''

    def _getRecastConversation(self):
        return self.conversation

    def insertUserInput(self, userinput):
        return self._getRecastConversation().insert_one(userinput)

    def removeUserInput(self):
        self._getRecastConversation().remove()

    def insertRecastResponse(self, recastresponse):
        return self._getRecastConversation().insert_one(recastresponse)

    def findAllUserInputs(self):
        return self._getRecastConversation().find()

    