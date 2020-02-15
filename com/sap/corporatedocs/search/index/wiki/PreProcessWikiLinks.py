from com.sap.corporatedocs.search.index.common.MongoDB import MongoDB
from com.sap.corporatedocs.search.index.common.ExtractPageLink import ExtractPageLink
import json
import bs4.element
from bs4 import BeautifulSoup

class PreProcessWikiLinks(object):
    def __init__(self):
        self.extractPageLink = ExtractPageLink()
        self.doc = ""
        self.link = ""
        self.title = ""
        self.lastModifiedDate = ""
        self.paragraph = ""
        self.outLinks = []
        self.mongoDB = MongoDB()
        self.mongoDB.connect()

    def createWikiLinkInfoJSON(self):
        doc = {}
        doc['link'] = self.link
        doc['title'] = self.title
        doc['lastModifiedDate'] = self.lastModifiedDate
        doc['paragraph'] = self.paragraph
        doc['outLinks'] = self.outLinks
        return json.loads(json.dumps(doc))
        
    def getTitle(self, htmlSoup):
        titleElemList = htmlSoup.find_all('title')
        return titleElemList[0].string
    
    def getLastModifiedDate(self, htmlSoup):
        lastModifiedDate = ""
        repElemList = htmlSoup.find_all('a')
        for repElem in repElemList:
            repElemID = repElem.get('class')
            if(repElemID != None and repElemID == ['last-modified']):
                lastModifiedDate = repElem.string
                break;
        return lastModifiedDate
    
    def getAllParagraphs(self, htmlSoup):
        paragraph = ""
        ''' This div contains all the text edited by authors 
            <div id="main-content" class="wiki-content"> '''
        divs = htmlSoup.find_all('div', 'wiki-content', id="main-content")
        try:
            ''' Some wiki pages have no contents just redirection to other wiki pages. Ignore them'''
            wikiContents = divs[0].contents
            for wikiContent in wikiContents:
                if(type(wikiContent) is bs4.element.Tag):
                    paragraph = paragraph + wikiContent.text
                else:
                    paragraph = paragraph + wikiContent.string
                ''' Add additional space between words '''
                paragraph = paragraph + " "
        except Exception:
            paragraph = ""
        return paragraph
    
    def getAllLinks(self, baseUrl, html_page):
        return self.extractPageLink.getFilteredPageLinks(baseUrl, html_page)
                
    def extractNSaveWikiLinkInfo(self):
        wikiLinks = self.mongoDB.findAllWikiLinks()
        for wikiLink in wikiLinks:
            self.doc = wikiLink['pagedata']
            htmlSoup = BeautifulSoup(self.doc, 'html.parser')
            '''Extract wiki link infos '''
            self.link = wikiLink['link']
            print(self.link)            
            self.title = self.getTitle(htmlSoup)
            self.lastModifiedDate = self.getLastModifiedDate(htmlSoup)
            self.paragraph = self.getAllParagraphs(htmlSoup)
            self.outLinks = self.getAllLinks("https://wiki.wdf.sap.corp/wiki/display/CoCo/", self.doc)
            '''Save wiki link infos ''' 
            self.mongoDB.insertWikiLinkInfo(self.createWikiLinkInfoJSON())

if(__name__ == "__main__"):
    preProcess = PreProcessWikiLinks()
    preProcess.extractNSaveWikiLinkInfo()