from elasticsearch import Elasticsearch

class TestNGPBugIndex(object):

    def __init__(self):
        self.eshost = "localhost"
        self.esport = 9200
        self.index = 'ngpbug-index'
        self.docType = 'ngpbug-docs'        
        self.es = Elasticsearch([{'host': self.eshost, 'port': self.esport}])
    
    def testGetDocByIndexedId(self, docId):
        doc = self.es.get(index=self.index, doc_type=self.docType, id=docId)
        contents = doc['_source']
        description = contents['description']
        print(description)
    
    def testGetDocByComponentId(self, componentId):
        docs = self.es.search(index=self.index, doc_type=self.docType, body={"query": {"match": {'component':componentId}}})
        print(docs['hits']['max_score'])
        print(docs['hits']['total'])
        hits = docs['hits']['hits']
        for hit in hits:
            print(hit['_source']['link'])                        
            print(hit['_source']['component'])            
            print(hit['_source']['description'])
    
    def testGetDocByFuzzySearch(self, pattern):
        docs = self.es.search(index=self.index, doc_type=self.docType, body={"query": {"prefix" : {'priority':pattern}}})
        print(docs['hits']['max_score'])
        print(docs['hits']['total'])
        hits = docs['hits']['hits']
        for hit in hits:
            print(hit['_source']['link'])                                    
            print(hit['_source']['priority'])
            print(hit['_source']['description'])

    def testGetDocByDescriptionSearch(self, pattern):
        docs = self.es.search(index=self.index, doc_type=self.docType, body={"query": {"match" : {'description':pattern}}})
        print(docs['hits']['max_score'])
        print(docs['hits']['total'])
        hits = docs['hits']['hits']
        for hit in hits:
            print(hit['_source']['link'])            
            print(hit['_source']['component'])
            print(hit['_source']['description'])
        
if __name__ == '__main__':
    test = TestNGPBugIndex()
    description = test.testGetDocByIndexedId(50)
    test.testGetDocByComponentId("BigData-Spark")
    test.testGetDocByFuzzySearch("Critical")
    test.testGetDocByDescriptionSearch("hcpbd-aws-canary-prod01")
