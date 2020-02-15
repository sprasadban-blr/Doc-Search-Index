# Getting started

<!-- markdownlint-disable MD001 MD022 -->
##### Table of Contents
<!-- markdownlint-enable MD001 MD022 -->

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Constraints](#constraints)

## Overview
Search index is enabled on corporate documents such as 'Wiki', 'NGP Bug tracker' and 'BCP incidents' in order to facilitate faster access of querying and retrieving the same.

Usage: The ChatBot and Search page (like Google) are the 2 applications envisaged at this point in time.

## Installation

### Prerequisites:  
1. Install Python 3.5.2 from this link https://www.python.org/downloads/release/python-352/:

		  ```
		  Set environment path variable based on your installation directory
		  C:\Python35\Lib\site-packages;
		  C:\Python35\Lib;
		  C:\Python35;
		  C:\Python35\DLLs;
		  C:\Python35\Scripts;

		  Test python version
		  $HOME_DIR: Can be any folder on your HDD
		  $HOME_DIR>python -V

		  Install needed packages for this application  
		  $HOME_DIR>pip install selenium
		  $HOME_DIR>pip install beautifulsoup4
		  $HOME_DIR>pip install urllib3
		  $HOME_DIR>pip install pymongo
		  $HOME_DIR>pip install flask  
		  $HOME_DIR>pip install flask-restful
		  $HOME_DIR>pip install elasticsearch
		  $HOME_DIR>pip install requests
		  $HOME_DIR>pip install wtforms
		  ```

2. Install MongoDB from this link https://www.mongodb.com/blog/post/mongodb-3-5-1-is-released:

		  ```
		   Note: MongoDB 3.6 has some issues in installing on Windows 10. 
		   Keep the default path as suggested by the installer 'C:\Program Files\MongoDB'   
		  ```

3. Install Chrome Driver from this link https://chromedriver.storage.googleapis.com/index.html?path=2.40/:
  
   The python selenium driver uses 'headless browser' for injecting user/password to wiki/ngpbug for the first accessed link.
	  ```
	  
	  Unzip and copy chrome driver to this location: 'C:\chrome_driver\chromedriver.exe'
	  
	  ```
4. Install ElasticSearch from this link https://www.elastic.co/downloads/past-releases/elasticsearch-6-2-2/:

 		```	
 		Note: Unzip and place at desired location. 
   		For Example: C:\D\ElasticSearch\elasticsearch-6.2.2
   		
 		``` 

5. Use code editor of your choice (Optional)

    ```    
  	 a) From Eclipse install PyDev modules from this link http://www.pydev.org/manual_101_install.html to work with python modules
   	 b) Download VSCode from this link https://code.visualstudio.com/docs/setup/windows
   	 c) Install Python for VSCode from this link https://code.visualstudio.com/docs/python/python-tutorial    	
    ```
    
## Usage

1. Start Mongo DB server
        ``` 	
 		
		   a) Start Mongo DB server from C:\Program Files\MongoDB\Server\3.4\bin>mongod
		   Note: Mongo DB server running on URL http://localhost:27017/
		   
		   b) Start Mongo Client from C:\Program Files\MongoDB\Server\3.4\bin>mongo
		   Note: Mongo DB client is needed to view records in the collections/tables.
    	``` 
2. Start elastic search server
	```
	
		C:\D\ElasticSearch\elasticsearch-6.2.2\bin>elasticsearch
	```    	
3. Add your windows user id and password in C:\Users\<<INO>>\github\doc_search_index\com\sap\corporatedocs\search\index\wiki\Connection.py file.
	```
	
		self.userId = '<<INo>>'
		self.passsword = '<<Password>>'
      
		Note: Once we get common user and password then we update here. We only need to change password as per corporate password change policy.
		    
    ```
    
4. Lookout 'chrome.exe' in your machine and change the file path in this file C:\Users\<<INo>>\github\doc_search_index\com\sap\corporatedocs\search\index\common\ChromeDriver.py
	```
	For Example: The following file are usually located in the below path. If you don't find it in your machine then uninstall and reinstall the Google Chrome Browser
 	
 	self.CHROME_BINARY_LOC = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
	
	```

5. Download wiki links, store into MongoDB, pre-process the data and index by using elastic search:
		 ``` 
		 
		 Execute following code 
		 $Source_Code_Location:>python WikiAll.py
		 '$Source_Code_Location'--> C:\Users\<<INO>>\github\doc_search_index\
		   
		 Note: It is time consuming activity and might take approximately 3 hours based on network speed
		   
      ```
6.  Download NGPBug links, store into MongoDB, pre-process the data and index by using elastic search:
           ```
           
        Execute following code 
        $Source_Code_Location:>python NGPBugAll.py
        '$Source_Code_Location'--> C:\Users\<<INO>>\github\doc_search_index\


		 Note: It is time consuming activity and might take approximately 6 hours based on network speed		      

	```
		 Note: Step 4 and 5 can run in parallel from different command prompt 
	```		
7. Start REST service which reads indexed records from elastic search:
   	    ```
   	    
        $Source_Code_Location:>python CorporateIndex.py
        '$Source_Code_Location'--> C:\Users\<<INO>>\github\doc_search_index\
        
        URL for wiki: http://127.0.0.1:5002/wiki/<<Search Query>> 
        URL for ngpbug: http://127.0.0.1:5002/ngpbug/<<Search Query>>
        
   		```

8. Start search query web page (like Google) to enter natural language query
		```
		
		$Source_Code_Location:>python DocgleWebForm.py
       '$Source_Code_Location'--> C:\Users\<<INO>>\github\doc_search_index\webapp
		 
		URL for search page: http://127.0.0.1:5000/sap
		
   		```
      
## Constraints

    1) Indexed only CoCo Wiki's.
    2) Indexed NGP Bug issues.
    2) BCP Incidents are currently not supported.