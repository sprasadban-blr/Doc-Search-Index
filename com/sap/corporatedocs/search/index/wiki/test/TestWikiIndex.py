from elasticsearch import Elasticsearch

class TestWikiIndex(object):

    def __init__(self):
        self.eshost = "localhost"
        self.esport = 9200
        self.index = 'wiki-index'
        self.docType = 'wiki-docs'        
        self.es = Elasticsearch([{'host': self.eshost, 'port': self.esport}])

    def testGetWikiDocByIndexedId(self, docId):
        doc = self.es.get(index=self.index, doc_type=self.docType, id=docId)
        contents = doc['_source']
        print(contents['paragraph'].encode('utf-8'))
        
    def testGetWikiDocByLinkId(self, linkId):
        docs = self.es.search(index=self.index, doc_type=self.docType, body={"query": {"match": {'link':linkId}}})
        print(docs['hits']['max_score'])
        print(docs['hits']['total'])
        hits = docs['hits']['hits']
        for hit in hits:
            print(hit['_source']['link'])                        
            print(hit['_source']['lastModifiedDate'])            
            print(hit['_source']['paragraph'].encode('utf-8'))        

    def testGetWikiDocByDescription(self, desc):
        docs = self.es.search(index=self.index, doc_type=self.docType, body={"query": {"match": {'paragraph':desc}}})
        print(docs['hits']['max_score'])
        print(docs['hits']['total'])
        hits = docs['hits']['hits']
        for hit in hits:
            print(hit['_source']['link'])                        
            print(hit['_source']['lastModifiedDate'])            
            print(hit['_source']['paragraph'].encode('utf-8'))
            
if __name__ == '__main__':
    wikiSearch = TestWikiIndex()
    wikiSearch.testGetWikiDocByIndexedId(100)
    wikiSearch.testGetWikiDocByLinkId("Messaging")
    wikiSearch.testGetWikiDocByDescription("hasso")        