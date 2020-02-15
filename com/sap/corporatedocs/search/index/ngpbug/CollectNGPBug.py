from com.sap.corporatedocs.search.index.common.MongoDB import MongoDB
from com.sap.corporatedocs.search.index.common.ChromeDriver import ChromeDriver
import json
from bs4 import BeautifulSoup
import os

class CollectNGPBug:
    def __init__(self):
        self.links = []
        self.driver = ChromeDriver()
        self.webdriver = self.driver.getChromeDriver()
        self.mongodb = MongoDB()
        self.mongodb.connect()
        self.link = ""

    def createNgpBugLinkJSON(self):
        doc = {}
        doc['link'] = self.link
        return json.loads(json.dumps(doc))

    def _getAllNGPBugs(self, startUrl):
        allNGPBugs = []
        html_page = self.driver.getUrlData(startUrl, "j_username", "j_password", "logOnFormSubmit")
        htmlSoup = BeautifulSoup(html_page, 'html.parser')
        ''' All NGP bugs are available in this div
            <div class="navigator-content" data-issue-table-model-state=" ...  
        '''        
        divs = htmlSoup.find_all('div', 'navigator-content')
        allNGPBugData = ""
        for div in divs:
            ''' Ignore any other sub div throws up exceptions '''
            try:
                allNGPBugData = div['data-issue-table-model-state']
                break
            except Exception:
                continue
        if(allNGPBugData == None or allNGPBugData.strip() == ''):
            return allNGPBugs
        ''' Convert JSON string to Python dictionary '''
        allNGPBugJson = json.loads(allNGPBugData)
        ''' All NGP bugs are in issuetable-->issuekeys segment '''
        allNGPBugs = allNGPBugJson['issueTable']['issueKeys']
        return allNGPBugs
    
    def _saveNGPBugLinks(self, baseUrl, allNGPBugs):
        for ngpbug in allNGPBugs:
            self.link = baseUrl + ngpbug
            self.links.append(self.link)
            print(self.link)
            self.mongodb.insertNGPBugLink(self.createNgpBugLinkJSON())

    def _saveNGPBugLinksToFile(self):
        path = os.getcwd() + "\\output\\ngpbugslinks.txt"        
        file = open(path, "w")
        for link in self.links:
            file.write(link)
            file.write("\n")
        file.close()

    def _removeNGPBugRecords(self):
        self.mongodb.removeNGPBugLink()
        self.mongodb.removeNGPBugData()
        self.mongodb.removeNGPBugLinkInfo()
        
    def collect(self, baseUrl, startUrl, cleanUpData):
        if(cleanUpData):
            self._removeNGPBugRecords()        
        allNGPBugs = self._getAllNGPBugs(startUrl)
        print(allNGPBugs)
        self._saveNGPBugLinks(baseUrl, allNGPBugs)
        self._saveNGPBugLinksToFile()
        
if __name__ == '__main__':
    baseUrl = "https://jtrack.wdf.sap.corp/browse/"
    startUrl = "https://jtrack.wdf.sap.corp/secure/IssueNavigator.jspa?reset=true&amp;mode=hide&amp;jqlQuery=project+%3D+NGPBUG"
    ngpCollector = CollectNGPBug();
    ngpCollector.collect(baseUrl, startUrl)
    
