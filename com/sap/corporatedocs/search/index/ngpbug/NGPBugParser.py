from com.sap.corporatedocs.search.index.common.ChromeDriver import ChromeDriver
from com.sap.corporatedocs.search.index.common.ExtractPageLink import ExtractPageLink
from com.sap.corporatedocs.search.index.common.MongoDB import MongoDB
import json
import os

class NGPBugParser(object):
    def __init__(self):
        self.processedNGPBugLinks = []
        self.driver = ChromeDriver()
        self.webdriver = self.driver.getChromeDriver()
        self.extractPageLink = ExtractPageLink() 
        self.mongodb = MongoDB()
        self.mongodb.connect()
        self.link = ""
        self.pagedata = ""         

    def createNgpBugJSON(self):
        doc = {}
        doc['link'] = self.link
        doc['pagedata'] = self.pagedata
        return json.loads(json.dumps(doc))
                        
    def _getAllProcessedNGPBugLinks(self):
        allProcessedNGPBugLinks = []
        processedNGPBugLinks = self.mongodb.findAllProcessedNGPBugData()
        for processedNGPBugLink in processedNGPBugLinks:
            allProcessedNGPBugLinks.append(processedNGPBugLink['link'])
        return allProcessedNGPBugLinks
        
    def _getAllNGPBugLinks(self):
        allBugLinks = []
        allAvailableNGPBugLinks = self.mongodb.findAllNGPBugLinks()
        for bugLink in allAvailableNGPBugLinks:
            allBugLinks.append(bugLink['link'])
        return allBugLinks
                
    def _parsePageLinks(self, baseUrl):
        '''Get page data'''
        html_page = self.driver.getUrlData(baseUrl, "j_username", "j_password", "logOnFormSubmit")
        '''Insert document '''
        self.link = baseUrl
        self.pagedata = html_page
        self.mongodb.insertNGPBugData(self.createNgpBugJSON())
        '''print(html_page.encode("utf-8"))'''
        return

    def _parseNGPBugLinks(self):
        allNGPBugLinks = self._getAllNGPBugLinks()
        self.processedNGPBugLinks = self._getAllProcessedNGPBugLinks()
        for aNGPBugLink in allNGPBugLinks:
            if(aNGPBugLink not in self.processedNGPBugLinks):
                print(aNGPBugLink)
                self._parsePageLinks(aNGPBugLink)
                self.processedNGPBugLinks.append(aNGPBugLink)            
            
    def _saveParsedFiles(self):
        path = os.getcwd() + "\\output\\ngpbugs.txt"        
        file = open(path, "w")
        for link in self.processedNGPBugLinks:
            file.write(link)
            file.write("\n")
        file.close()
    
    def parse(self):
        self._parseNGPBugLinks()
        self._saveParsedFiles()
                    
if(__name__ == "__main__"):
    ngpParser = NGPBugParser();
    ngpParser.parse()
