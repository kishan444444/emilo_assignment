# app/faiss_db.py

import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

# Load data
with open("project/data/final.json", "r", encoding="utf-8") as f:
    products = json.load(f)


def build_text(p):
    return (
        f"{p.get('name','')} "
        f"{p.get('description','')} "
        f"{p.get('shortDescription','')} "
        f"{p.get('brand','')}"
    ).lower()


# Preprocess
for p in products:
    p["searchText"] = build_text(p)
    p["embedding"] = model.encode(p["searchText"])


# Build FAISS
embeddings = np.array([p["embedding"] for p in products]).astype("float32")
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)


def search_faiss(query, top_k=50):
    query_embedding = model.encode(query).astype("float32")
    _, indices = index.search(np.array([query_embedding]), top_k)
    return [products[i] for i in indices[0]]

