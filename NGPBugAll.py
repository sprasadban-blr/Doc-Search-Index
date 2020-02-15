from com.sap.corporatedocs.search.index.ngpbug.NGPBugParser import NGPBugParser
from com.sap.corporatedocs.search.index.ngpbug.CollectNGPBug import CollectNGPBug
from com.sap.corporatedocs.search.index.ngpbug.PreProcessNGPBugLink import PreProcessNGPBugLink
from com.sap.corporatedocs.search.index.ngpbug.NGPBugIndexer import NGPBugIndexer

class NGPBugAll(object):
    
    def __init__(self):
        self.BASE_URL = "https://jtrack.wdf.sap.corp/browse/"
        self.START_URL = "https://jtrack.wdf.sap.corp/secure/IssueNavigator.jspa?reset=true&amp;mode=hide&amp;jqlQuery=project+%3D+NGPBUG"
        self.collectNgpBug = CollectNGPBug()        
        self.ngpBugParser = NGPBugParser()
        self.preProcessNgpBug = PreProcessNGPBugLink()
        self.ngpBugIndexer = NGPBugIndexer()
    
    def executeAll(self):
        ''' Collect all NGP Bug link details '''
        self.collectNgpBug.collect(self.BASE_URL, self.START_URL, True)
        ''' Parse relevant NGP Bug link details '''        
        self.ngpBugParser.parse()
        ''' Preprocess NGP Bug link details '''                
        self.preProcessNgpBug.extractNSaveNGPBugLinkInfo()
        ''' Index NGP Bug link details '''        
        self.ngpBugIndexer.indexNGPBugLinkInfo(True)
        
    
if __name__ == '__main__':
    ngpBugAll = NGPBugAll()
    ngpBugAll.executeAll()      