''' pip install selenium '''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from com.sap.corporatedocs.search.index.common.Connection import Connection
import os

class ChromeDriver(object):
    def __init__(self):
        self.CHROME_BINARY_LOC = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
        self.CHROME_DRIVER_PATH = r'C:\chrome_driver\chromedriver.exe'
        chrome_options = Options()  
        chrome_options.add_argument("--headless")  
        chrome_options.binary_location = self.CHROME_BINARY_LOC
        chromeDriverPath = self.CHROME_DRIVER_PATH
        self.webdriver = webdriver.Chrome(executable_path=os.path.abspath(chromeDriverPath), chrome_options=chrome_options)
        self.connection = Connection();        
   
    def getChromeDriver(self):
        return self.webdriver
    
    def getUrlData(self, url, userElement, passwordElement, loginButtonElement):
        self.webdriver.get(url)
        '''print(self.webdriver.page_source.encode("utf-8"))'''
        self.logon(userElement, passwordElement, loginButtonElement)        
        return self.webdriver.page_source
            
    def logon(self, userElement, passwordElement, loginButtonElement):
        if(self.checkElementExits(userElement)):
            self.webdriver.find_element_by_id(userElement).clear()
            self.webdriver.find_element_by_id(userElement).send_keys(self.connection.getUserId())
        if(self.checkElementExits(passwordElement)):
            self.webdriver.find_element_by_id(passwordElement).clear();
            self.webdriver.find_element_by_id(passwordElement).send_keys(self.connection.getPassword());
        if(self.checkElementExits(loginButtonElement)):
            self.webdriver.find_element_by_id(loginButtonElement).click();
        
    def checkElementExits(self, elementName):
        try:
            self.webdriver.find_element_by_id(elementName)
            return True
        except NoSuchElementException:
            return False        
