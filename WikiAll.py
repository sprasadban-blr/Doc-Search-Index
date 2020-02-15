from com.sap.corporatedocs.search.index.wiki.WikiParser import WikiParser
from com.sap.corporatedocs.search.index.wiki.WikiIndexer import WikiIndexer
from com.sap.corporatedocs.search.index.wiki.PreProcessWikiLinks import PreProcessWikiLinks

class WikiAll():
    def __init__(self, baseURL):
        self.BASE_URL = baseURL
        self.wikiParser = WikiParser()
        self.wikiPreProcess = PreProcessWikiLinks()
        self.wikiIndexer = WikiIndexer()        
    
    def executeAll(self):
        ''' Collect all wiki link details and store in MongoDB'''
        self.wikiParser.parse(self.BASE_URL, True)   
        
        ''' Pre process wiki links '''
        self.wikiPreProcess.extractNSaveWikiLinkInfo()
        
        ''' Index wiki details into elastic search '''
        self.wikiIndexer.indexWikiLinksInfo(True)

if __name__ == '__main__':
    baseUrl = "https://wiki.wdf.sap.corp/wiki/display/CoCo/"    
    wiki = WikiAll(baseUrl)
    wiki.executeAll()        