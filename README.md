
## 📘 Project: Semantic Search & Information Extraction (IE) Prototype

This project implements an end-to-end prototype for semantic search and information extraction from PDF documents using NLP and graph technologies.

---

## ❓ What is Information Extraction (IE)?
**Information Extraction (IE)** refers to the process of automatically pulling out structured information from unstructured text — such as named entities (people, organizations, dates) and their relationships.

## 🧠 What is Semantic Search?
**Semantic search** goes beyond keyword matching — it uses the *meaning* behind words and structure of content to return more relevant results.

---

## 🧩 What This Project Does (High Level)
1. Takes in a PDF
2. Extracts raw text using Apache Tika
3. Uses spaCy (transformer model) to:
   - Identify named entities
   - Extract relationships between them
4. Indexes the document and entities in Elasticsearch
5. Creates a knowledge graph of entities + their connections in Neo4j
6. Serves a REST API with:
   - `/ingest` to upload and process new files
   - `/search` to query across documents and entities

---

## 🧱 Tech Stack
| Purpose                | Tool/Library       |
|------------------------|--------------------|
| Text Extraction        | Apache Tika        |
| NLP / NER / Relations  | spaCy (en_core_web_trf) |
| Search Engine          | Elasticsearch      |
| Knowledge Graph        | Neo4j              |
| REST API               | FastAPI            |
| Deployment             | Docker + Compose   |

---

## 🗂 File Structure
```
├── data_ingest.py        # Extract text from PDFs using Tika
├── nlp_pipeline.py       # Named entity and relation extraction with spaCy
├── indexer.py            # Index documents/entities into Elasticsearch
├── graph_builder.py      # Build graph from entities + relations in Neo4j
├── api.py                # FastAPI app: /ingest and /search
├── requirements.txt      # Python dependencies
├── Dockerfile            # Build script for FastAPI app
├── docker-compose.yml    # Spin up app + services (ES, Neo4j)
└── README.md             # You're reading it!
```

---

## 🚀 Setup & Run
### 1. Prerequisites
- Docker
- Docker Compose

### 2. Launch the Full Stack
```bash
docker-compose up --build
```

- FastAPI API will be available at: http://localhost:8000
- Elasticsearch: http://localhost:9200
- Neo4j UI: http://localhost:7474 (login: `neo4j` / `test`)

---

## ⚙️ Usage
### 📄 Upload a PDF
```bash
POST /ingest
```
- Send a PDF file
- It will:
  - Extract text
  - Extract entities & relations
  - Index content in Elasticsearch
  - Build knowledge graph in Neo4j

### 🔍 Search
```bash
GET /search?q=<your query>&top_k=5
```
- Returns top-K documents matching the query across:
  - Full-text content
  - Named entities

---

## 🔁 Example Flow
```
PDF → Tika → spaCy → [ Entities, Relations ]
 → Elasticsearch Index
 → Neo4j Graph
 → FastAPI APIs to ingest/search
```

---

## 🧠 Sample Use Case
Imagine uploading research papers or patent documents. You can:
- Search for "AI and energy startups"
- Extract and connect key players, dates, products
- Visualize relations (who funded whom, which tech uses what)

---

## 🧪 Next Steps (Optional Enhancements)
- Use Graph Neural Networks (PyTorch Geometric) to cluster similar documents
- Add frontend UI
- Enable entity linking or disambiguation

---

## 🙌 Author
Koushik Samudrala

Feel free to fork, modify, and share. PRs welcome!

---

## 📜 License
MIT License
