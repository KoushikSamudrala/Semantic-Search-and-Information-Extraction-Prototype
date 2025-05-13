# Project: Semantic Search & Information Extraction Prototype

This repository provides a modular, end-to-end pipeline to:
- Ingest PDF text
- Extract entities & relations using spaCy
- Index documents in Elasticsearch
- Build a Neo4j knowledge graph
- Serve a FastAPI API for /ingest and /search

## File Structure
```
├── README.md
├── data_ingest.py
├── nlp_pipeline.py
├── indexer.py
├── graph_builder.py
├── api.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## Setup & Run
1. Install Docker & Docker Compose
2. Clone this repo
docker-compose up --build
3. API at http://localhost:8000



Semantic Search & Information Extraction (IE) Prototype

✅ What the name means:
Semantic Search = Search that understands meaning, not just keywords.

Information Extraction (IE) = Automatically finding useful facts (e.g., names, dates, relationships) from text.

So, this project helps you upload a PDF, then:

Pulls out useful information (like names of people, organizations, locations).

Understands who is related to what (relations).

Stores that information in searchable ways.

Lets you search using meaning—like “find PDFs mentioning research labs that partnered with Tesla.”

🧠 Big Picture: What Does It Do?
You upload PDFs → it extracts meaning → builds a smart index → lets you search that meaning.

📁 Project Structure – What Each Part Does
1. data_ingest.py – Extract Text from PDF
Uses Apache Tika to convert PDF to plain text.

PDF in → Clean, readable text out.

🧱 Fundamental Principle: All downstream AI tasks need clean text as input.

2. nlp_pipeline.py – Understand Text with NLP
Uses spaCy to do:

NER (Named Entity Recognition): finds names of people, places, etc.

Relation Extraction: simple logic to find “X uses Y” or “A works with B” sentences.

📌 This gives us entities and relationships that represent meaning.

Example:

From: "Tesla partnered with Samsung in 2022."
It might extract:

Entities: Tesla (ORG), Samsung (ORG), 2022 (DATE)

Relation: Tesla —[partnered_with]→ Samsung

3. indexer.py – Store in Searchable Form
Sets up an Elasticsearch index (like a smart, searchable database).

Indexes:

Raw text

Named entities

Filename (PDF name)

💡 This lets you search not only for “battery” but also for documents containing entities like “Panasonic”.

4. graph_builder.py – Build a Knowledge Graph
Uses Neo4j, a database for storing networks of connected things.

Every entity becomes a node.

Every relationship becomes a connection (edge).

So now you can visually or programmatically explore things like:

“What companies are connected to Tesla?”
“What topics link Germany and 2023?”

5. api.py – FastAPI Web Interface
Defines:

POST /ingest → You upload a PDF, it runs the whole pipeline.

GET /search?q=... → You search across content + extracted entities.

This makes it usable from a browser, web app, or another system.

6. Dockerfile + docker-compose.yml
These help run everything easily with one command using Docker:

Elasticsearch

Neo4j

Your FastAPI app

You don’t need to install anything manually. It’s all containerized.

🧩 Summary of Core Components and Their Purpose
Module	What It Does	Core Concepts Used
data_ingest.py	PDF → Text	Apache Tika
nlp_pipeline.py	Text → Entities + Relationships	spaCy, NER, dependency parsing
indexer.py	Save searchable content + metadata	Elasticsearch
graph_builder.py	Save structured knowledge as a graph	Neo4j, nodes & edges
api.py	Offer HTTP endpoints for ingestion and search	FastAPI
Dockerfile	Package Python app	Docker
docker-compose	Orchestrate multiple services	Docker Compose (ES, Neo4j, API together)

🧠 First-Principles Thinking: Why This Approach Works
Text is unstructured. We first clean it and extract structure (entities, relations).

Structure enables search. Search engines (like Elasticsearch) and graphs (like Neo4j) work best when data has structure.

APIs enable integration. Any app can now interact with this system by uploading PDFs or searching.

🧪 Sample Use Case
Let’s say you have 100 scientific research papers in PDF. You want to:

Find documents mentioning "AI + manufacturing".

List all people/organizations involved.

See how companies like Bosch are connected to other entities.

This project: ✅ Extracts facts
✅ Connects the dots
✅ Lets you explore and query meaningfully

