from elasticsearch import Elasticsearch

class ESCrud:
    def __init__(self, host='localhost', port=9200, scheme='http'):
        # Correctly set up the connection with a scheme
        self.es = Elasticsearch(
            hosts=[{"host": host, "port": port, "scheme": scheme}]
        )

    def create_index(self, index_name, settings):
        """Create an index with specific settings and mappings."""
        self.es.indices.create(index=index_name, body=settings, ignore=400)

    def insert_document(self, index_name, document, doc_id=None):
        """Insert a document into a specified index."""
        return self.es.index(index=index_name, id=doc_id, document=document)

    def get_document(self, index_name, doc_id):
        """Retrieve a document by ID from a specified index."""
        return self.es.get(index=index_name, id=doc_id)

    def update_document(self, index_name, doc_id, doc_update):
        """Update a document by ID."""
        return self.es.update(index=index_name, id=doc_id, body={'doc': doc_update})

    def delete_document(self, index_name, doc_id):
        """Delete a document by ID."""
        return self.es.delete(index=index_name, id=doc_id)
