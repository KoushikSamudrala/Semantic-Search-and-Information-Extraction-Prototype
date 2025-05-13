import io
from tika import parser
import spacy
from elasticsearch import Elasticsearch
from neo4j import GraphDatabase
from fastapi import FastAPI, UploadFile, File, HTTPException

# ----- Configuration -----
ES_HOST = 'elasticsearch'
ES_PORT = 9200
ES_INDEX = 'documents'
NEO4J_URI = 'bolt://neo4j:7687'
NEO4J_AUTH = ('neo4j', 'test')

# ----- PDF Ingestion -----
def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """
    Parse PDF bytes using Apache Tika and return extracted plain text.
    """
    parsed = parser.from_buffer(pdf_bytes)
    return parsed.get('content', '')

# ----- NLP Pipeline (spaCy) -----
nlp = spacy.load("en_core_web_trf")

def extract_entities_and_relations(text: str):
    """
    Run spaCy NER and simple relation extraction on input text.
    Returns: entities list[(str,label)], relations list[(subj, pred, obj)].
    """
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    relations = []
    for sent in doc.sents:
        for token in sent:
            if token.dep_ in ('relcl', 'prep'):
                subj = [w for w in token.head.lefts if w.dep_ in ('nsubj','nsubjpass')]
                obj = [w for w in token.rights if w.dep_ in ('dobj','pobj')]
                if subj and obj:
                    relations.append((subj[0].text, token.head.lemma_, obj[0].text))
    return entities, relations

# ----- Elasticsearch Indexing -----
es = Elasticsearch([{'host': ES_HOST, 'port': ES_PORT}])

def create_es_index():
    """Create Elasticsearch index with mapping for content and entities."""
    mapping = {
        'mappings': {
            'properties': {
                'content': {'type': 'text', 'analyzer': 'english'},
                'entities': {
                    'type': 'nested',
                    'properties': {
                        'text': {'type': 'keyword'},
                        'label': {'type': 'keyword'}
                    }
                },
                'path': {'type': 'keyword'}
            }
        }
    }
    es.indices.create(index=ES_INDEX, body=mapping, ignore=400)


def index_document(path: str, content: str, entities: list):
    """Index a document with content and extracted entities into Elasticsearch."""
    doc = {
        'path': path,
        'content': content,
        'entities': [{'text': e[0], 'label': e[1]} for e in entities]
    }
    es.index(index=ES_INDEX, body=doc)

# ----- Neo4j Knowledge Graph -----
driver = GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH)

def build_knowledge_graph(entities, relations):
    """Build nodes and relationships in Neo4j from extracted entities/relations."""
    with driver.session() as session:
        for name, label in entities:
            session.run(
                "MERGE (e:Entity {name: $name, label: $label})",
                {'name': name, 'label': label}
            )
        for subj, pred, obj in relations:
            session.run(
                "MATCH (s:Entity {name: $s}), (o:Entity {name: $o}) \
                 MERGE (s)-[r:REL {type: $pred}]->(o)",
                {'s': subj, 'pred': pred, 'o': obj}
            )

# ----- FastAPI Application -----
app = FastAPI()

# Ensure ES index exists on startup
def init():
    create_es_index()

@app.on_event("startup")
async def startup_event():
    init()

@app.post("/ingest")
async def ingest_pdf(file: UploadFile = File(...)):
    """
    Ingest a PDF: extract text, entities, relations, index in ES, and build KG.
    Returns counts of extracted items.
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files supported.")
    data = await file.read()
    text = extract_text_from_pdf_bytes(data)
    entities, relations = extract_entities_and_relations(text)
    index_document(file.filename, text, entities)
    build_knowledge_graph(entities, relations)
    return {
        'message': 'Document ingested',
        'entities': len(entities),
        'relations': len(relations)
    }

@app.get("/search")
def search_documents(q: str, top_k: int = 10):
    """
    Search indexed documents by query string over content & entities.
    Returns top_k hits with path + score.
    """
    body = {
        'query': {
            'multi_match': {
                'query': q,
                'fields': ['content', 'entities.text']
            }
        },
        'size': top_k
    }
    res = es.search(index=ES_INDEX, body=body)
    results = []
    for hit in res['hits']['hits']:
        results.append({
            'path': hit['_source']['path'],
            'score': hit['_score']
        })
    return {'results': results}

# Entry point for Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)