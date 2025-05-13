from elasticsearch import Elasticsearch
# Elasticsearch client
es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])
INDEX = 'documents'

def create_es_index():
    mapping = {
        'mappings': {'properties': {
            'content': {'type': 'text', 'analyzer': 'english'},
            'entities': {'type': 'nested', 'properties': {
                'text': {'type': 'keyword'}, 'label': {'type': 'keyword'}
            }},
            'path': {'type': 'keyword'}
        }}
    }
    es.indices.create(index=INDEX, body=mapping, ignore=400)

def index_document(path: str, content: str, entities: list):
    doc = {
        'path': path,
        'content': content,
        'entities': [{'text': e[0], 'label': e[1]} for e in entities]
    }
    es.index(index=INDEX, body=doc)