#Selenium Doc: http://selenium-python.readthedocs.io/locating-elements.html
#Elastic Search: https://tryolabs.com/blog/2015/02/17/python-elasticsearch-first-steps/

from com.sap.corporatedocs.search.index.common.ChromeDriver import ChromeDriver
from com.sap.corporatedocs.search.index.common.ExtractPageLink import ExtractPageLink
from com.sap.corporatedocs.search.index.common.MongoDB import MongoDB
import json
import os

class WikiParser(object):
    def __init__(self):
        self.visited = []
        self.driver = ChromeDriver()
        self.extractPageLink = ExtractPageLink()
        self.mongodb = MongoDB()
        self.mongodb.connect()
        self.link = ""
        self.pagedata = "" 
    
    def _createWikiDocJSON(self):
        doc = {}
        doc['link'] = self.link
        doc['pagedata'] = self.pagedata
        return json.loads(json.dumps(doc))
               
    def getPageLinks(self, baseUrl, html_page):
        return self.extractPageLink.getFilteredPageLinks(baseUrl, html_page)

    def _parsePageLinks(self, baseUrl):
        '''Already parsed'''
        if(baseUrl in self.visited):
            return
        print(baseUrl)
        self.visited.append(baseUrl)
        html_page = self.driver.getUrlData(baseUrl, "os_username", "os_password", "loginButton")
        '''Insert document '''
        self.link = baseUrl
        self.pagedata = html_page
        self.mongodb.insertWikiData(self._createWikiDocJSON())
        '''print(html_page.encode("utf-8"))'''
        pageLinks = self.getPageLinks(baseUrl, html_page)
        '''print(pageLinks)'''
        for pageLink in pageLinks:
            if(pageLink not in self.visited):
                '''print(pageLink)'''
                self._parsePageLinks(pageLink)
        return
    
    def getAllParsedPageLinks(self):
        return self.visited
    
    def _removeWikiRecords(self):
        self.mongodb.removeWikiData()
        self.mongodb.removeWikiLinkInfo()
        
    def _saveParsedFiles(self):
        path = os.getcwd() + "\\output\\wikilinks.txt"    
        file = open(path, "w")
        for link in self.visited:
            file.write(link)
            file.write("\n")            
        file.close()
        
    def parse(self, baseUrl, cleanUpData):
        if(cleanUpData):
            self._removeWikiRecords()
        self._parsePageLinks(baseUrl)
        self._saveParsedFiles()    

if(__name__ == "__main__"):
    wikiparser = WikiParser()
    baseUrl = "https://wiki.wdf.sap.corp/wiki/display/CoCo/"
    wikiparser.parse(baseUrl)
    allWikiLinks = wikiparser.getAllParsedPageLinks()
    print(allWikiLinks)
