from com.sap.corporatedocs.search.index.common.MongoDB import MongoDB
from bs4 import BeautifulSoup
import json
import bs4.element
import re

class PreProcessNGPBugLink(object):
    def __init__(self):
        self.link = ""
        self.type = ""
        self.priority = ""
        self.component = ""
        self.status = ""
        self.description = ""
        self.comments = ""
        self.mongoDB = MongoDB()
        self.mongoDB.connect()
    
    def createNGPBugLinkInfoJSON(self):
        doc = {}
        doc['link'] = self.link
        doc['type'] = self.type
        doc['priority'] = self.priority
        doc['component'] = self.component
        doc['status'] = self.status
        doc['description'] = self.description
        doc['comments'] = self.comments        
        return json.loads(json.dumps(doc))
        
    def getNGPBugInfo(self, htmlSoup, tagName, styleClassName, tagId, trimCarriageReturn=True):
        typeValue = ""
        ''' Finding exact html tag '''
        spanData = htmlSoup.find(tagName, styleClassName, id=tagId)
        if(spanData == None):
            return typeValue
        if(type(spanData) is bs4.element.Tag):
            typeValue = spanData.text
        else:
            typeValue = spanData.string
        ''' By default remove all carriage returns and special characters '''
        if(trimCarriageReturn):
            typeValue = re.sub('\s+', '', typeValue)
        return typeValue
    
    def getCommentsList(self, htmlSoup, tagName, styleClassName):
        commentsList = []
        allComments = htmlSoup.find_all(tagName, styleClassName)
        for comment in allComments:
            if(type(comment) is bs4.element.Tag):
                commentsList.append(comment.text)
            else:
                commentsList.append(comment.string)
        return commentsList
        
            
    def extractNSaveNGPBugLinkInfo(self):
        allNGPBugData = self.mongoDB.findAllNGPBugData()
        for aNGPBugData in allNGPBugData:
            self.link = aNGPBugData['link']
            print(self.link)
            pageData = aNGPBugData['pagedata']
            htmlSoup = BeautifulSoup(pageData, 'html.parser')
            self.type = self.getNGPBugInfo(htmlSoup, "span", "value", "type-val")
            self.priority = self.getNGPBugInfo(htmlSoup, "span", "value", "priority-val")
            self.component = self.getNGPBugInfo(htmlSoup, "span", "shorten", "components-field")
            self.status = self.getNGPBugInfo(htmlSoup, "span", "value", "status-val")
            self.description = self.getNGPBugInfo(htmlSoup, "div", "field-ignore-highlight", "description-val", False)
            self.comments = self.getCommentsList(htmlSoup, "div", "action-body flooded")
            self.mongoDB.insertNGPBugLinkInfo(self.createNGPBugLinkInfoJSON())
    
if __name__ == '__main__':
    preProcess = PreProcessNGPBugLinks()
    preProcess.extractNSaveNGPBugLinkInfo()        