''' pip install selenium '''
''' pip install beautifulsoup4 '''
''' pip install urllib3 '''
from bs4 import BeautifulSoup
from urllib import parse

class ExtractPageLink(object):
    
    def __init__(self) :
        self.whiteListedLinks = [
            "https://wiki.wdf.sap.corp/wiki/display/CoCo/",
            "https://jtrack.wdf.sap.corp/browse/NGPBUG-"
        ]
        self.filteredTags = [
            "createpage.action?",
            "editpage.action?",
            "dashboard.action",
            "showComments=true",
            "showCommentArea=true",
            "#addcomment",
            "/wiki/display/~",
            "?actionOrder=desc",
            "?actionOrder=asc",
            "?page=com.atlassian.jira.plugin.system.issuetabpanels",
            "?page=com.atlassian.streams.streams-jira-plugin",
            "?page=com.googlecode.jira-suite-utilities",
            "?focusedCommentId=",
            "?attachmentSortBy=",
            "?attachmentOrder=",
        ]
    
    def getAllPageLinks(self, baseUrl, html_page):
        links = []
        soup = BeautifulSoup(html_page)
        for link in soup.findAll('a', href=True):
            absUrl = parse.urljoin(baseUrl, link['href'])
            links.append(absUrl)
        return links

    def _isFilteredTags(self, link):
        isFiltered = False
        for filteredTag in self.filteredTags:
            if(filteredTag in link):
                isFiltered = True
                break
        return isFiltered
            
    def _isWhiteListedLink(self, link):
        isWhiteListed = False
        for whiteListedLink in self.whiteListedLinks:
            if(whiteListedLink in link):
                isWhiteListed = True
                break
        return isWhiteListed
    
    def getFilteredPageLinks(self, baseUrl, html_page):
        links = []
        soup = BeautifulSoup(html_page)
        for link in soup.findAll('a', href=True):
            orgLink = link['href']
            '''Eliminate bread crumbs, title-heading, menu bars, profile page, comments sections e.t.c '''
            if(orgLink.startswith('#') or self._isFilteredTags(orgLink)):
                continue
            absUrl = parse.urljoin(baseUrl, orgLink)
            ''' Look for White Listed links '''
            if(self._isWhiteListedLink(absUrl)):
                ''' Remove Duplicates '''
                if(absUrl != baseUrl and absUrl not in links):
                    links.append(absUrl)
        return links