from fastapi import FastAPI, UploadFile, File, HTTPException
from data_ingest import extract_text_from_pdf_bytes
from nlp_pipeline import extract_entities_and_relations
from indexer import create_es_index, index_document, es
from graph_builder import build_knowledge_graph

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    create_es_index()

@app.post("/ingest")
async def ingest_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(400, "Only PDF files supported.")
    data = await file.read()
    text = extract_text_from_pdf_bytes(data)
    entities, relations = extract_entities_and_relations(text)
    index_document(file.filename, text, entities)
    build_knowledge_graph(entities, relations)
    return {'message':'Indexed', 'entities':len(entities),'relations':len(relations)}

@app.get("/search")
def search_documents(q: str, top_k: int = 10):
    body = {
        'query': {'multi_match': {'query':q,'fields':['content','entities.text']}},
        'size': top_k
    }
    res = es.search(index='documents', body=body)
    return {'results':[{'path':h['_source']['path'],'score':h['_score']} for h in res['hits']['hits']]}