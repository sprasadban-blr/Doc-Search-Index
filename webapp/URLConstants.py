class URLConstants(object):
    def __init__(self):
        self.WIKI_URL = 'http://10.53.216.88:5002/wiki/'
        self.NGPBUG_URL = 'http://10.53.216.88:5002/ngpbug/'
        self.BCP_INCIDENT_URL = "http://10.53.216.88:5002/bcp/"
    
    def getWikiURL(self):
        return self.WIKI_URL
    
    def getNGPBugURL(self):
        return self.NGPBUG_URL
    
    def getBCPIncidentURL(self):
        return self.BCP_INCIDENT_URL    

