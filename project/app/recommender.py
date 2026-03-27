# app/recommender.py

from project.logger import logging
from project.exception import customexception
import sys
from .faiss_db import search_faiss, model
from .utils import cosine_similarity, normalize_score, get_score_label
from .llm import understand_query_llm, generate_reason_llm


def recommend_by_occasion(user_input, top_k=10):

    try:
        original_query = user_input.lower()
        user_input = understand_query_llm(original_query)

        candidates = search_faiss(user_input, top_k=50)

        query_embedding = model.encode(user_input)

        results = []

        for p in candidates:

            if not p.get("isValid", True):
                continue

            sim_score = cosine_similarity(query_embedding, p["embedding"])

            occasion_score = sum(
                0.3 for tag in p.get("occasionTags", [])
                if tag in user_input
            )

            tag_score = sum(
                0.1 for tag in p.get("tags", [])
                if tag in user_input
            )

            raw_score = sim_score + occasion_score + tag_score

            results.append((raw_score, p))

        results.sort(key=lambda x: x[0], reverse=True)

        output = []

        for raw_score, p in results[:top_k]:

            score = normalize_score(raw_score)
            label = get_score_label(score)

            desc = p.get("shortDescription") or p.get("description", "")

            reason = generate_reason_llm(p, user_input)

            output.append({
                "title": p.get("name"),
                "category": f'{p.get("categoryId")} ("{p.get("name")}")',
                "description": desc[:120] + "...",
                "image": p.get("mainImage"),
                "score": round(score, 2),
                "match": label,
                "reason": reason
            })

        return output
    except Exception as e:
                logging.info("Exception occured in load_object file utils")
                raise customexception(e,sys)
    
