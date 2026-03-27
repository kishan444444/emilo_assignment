# app/schemas.py

from pydantic import BaseModel
from typing import List

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5


class ProductResponse(BaseModel):
    title: str
    category: str
    description: str
    image: str
    score: float
    match: str
    reason: str


class QueryResponse(BaseModel):
    results: List[ProductResponse]