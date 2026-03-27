# 🎁 Occasion-Based Product Recommendation System

## 🚀 Overview
This project implements an AI-powered recommendation system that suggests relevant products based on a user-provided occasion (e.g., Birthday, Wedding, Diwali, Valentine’s Day, Office Party).

The system uses a **hybrid approach** combining semantic search, rule-based boosting, vector search (FAISS), and LLM capabilities to deliver accurate, fast, and explainable recommendations.

---

## 🧠 Approach

### 🔍 1. Embedding-Based Semantic Search
- Used **Sentence Transformers (`all-MiniLM-L6-v2`)**
- Generated embeddings for:
  - Product data (`name + description + shortDescription + brand`)
  - User query

**Why?**
- Captures meaning instead of exact words
- Works even if query wording is different

**Example:**
"romantic gift" ≈ "valentine gift"

---

### ⚡ 2. Vector Search using FAISS
- Built a FAISS index on product embeddings
- Retrieved only **top_k (~50)** most similar products

**Why?**
- Faster than scanning full dataset
- Scales to large data
- Improves performance

---

### 🏷️ 3. Tag-Based Boosting
Each product contains:
- `tags`
- `occasionTags`

**Boost Logic:**
- Occasion match → +0.3
- Tag match → +0.1

**Why?**
- Adds business logic
- Improves precision
- Prioritizes important occasions

---

### 🧮 4. Hybrid Scoring

Final score is calculated as:

Final Score = Similarity + Occasion Boost + Tag Boost

- Score normalized to range **0–1**
- Labels:
  - 0.3 → Weak match
  - 0.6 → Good match
  - 0.8+ → Strong match
  - 1.0+ → Very strong 🔥

---

### 🤖 5. LLM Query Understanding (Groq LLaMA)
- Converts messy user queries into standard occasions

**Examples:**
- "gift for girlfriend" → "valentine gift"
- "corporate present" → "office party gift"
- "festival shopping" → "diwali gift"

**Why?**
- Handles real-world queries
- Improves intent understanding

---

### 💬 6. LLM-Based Explanation
Each product includes a generated explanation:

Example:
"Recommended because it is ideal for Diwali gifting and festive celebrations."

**Why?**
- Improves user trust
- Makes system explainable
- Similar to Amazon/Netflix recommendations

---

## 🏗️ System Architecture

User Query  
↓  
LLM → Query Understanding  
↓  
FAISS → Candidate Retrieval  
↓  
Embedding Similarity  
↓  
Tag + Occasion Boost  
↓  
Final Ranking  
↓  
LLM → Explanation  
↓  
FastAPI Response  

---
##  Project Structure 
project/
│
├── app/
│ ├── main.py # FastAPI entry point + routes + HTML UI
│ ├── recommender.py # Core recommendation logic
│ ├── faiss_db.py # FAISS index & search
│ ├── llm.py # LLM query understanding + explanation
│ ├── utils.py # Helper functions (scoring, similarity)
│ ├── schemas.py # API schemas (Pydantic)
│
├── data/
│ └── products.json # Product dataset
│
├── Notebook files 
├  └──  data_preperation.ipynb # Data cleaning + tag generation 
│  └──  model_training.ipynb # Embedding + FAISS experiments
├── requirements.txt # Dependencies
├── README.md # Documentation

---

## 📦 Features

- Occasion-based recommendations  
- Semantic understanding (AI embeddings)  
- Fast retrieval using FAISS  
- Hybrid scoring system  
- LLM-powered query understanding  
- AI-generated explanations  
- Scalable architecture  

---

## 📊 Output Format

Each recommended product contains:

- Title  
- Category  
- Description snippet  
- Product Image  
- Score (0–1)  
- Match Label (Weak / Good / Strong / Very Strong)  
- Explanation  

---

## ⚖️ Design Decisions

- Hybrid model → best balance of accuracy and performance  
- FAISS (top_k = 50) → efficient candidate selection  
- Limited LLM usage → reduces cost and latency  
- Tag boosting → improves recommendation quality  

---

## 🚀 Future Improvements

- User personalization (history-based recommendations)  
- Multi-language support (Hindi + English)  
- LLM-based tag generation  
- Advanced LLM re-ranking  
- Category name mapping (instead of IDs)  

---

## 👨‍💻 How to Run

1. Activate environment
venv\Scripts\activate

2. Install dependencies
pip install -r requirements.txt

3. Run server
uvicorn main:app --reload 

4. Open browser
http://127.0.0.1:8000/

---

## 🧠 Conclusion

This system combines:

- Embeddings → semantic understanding  
- FAISS → fast search  
- Rules → better precision  
- LLM → intelligence + explanation  

Final Result:
- Accurate recommendations  
- Fast performance  
- Explainable outputs  
- Production-ready system  

---
