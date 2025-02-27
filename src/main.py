from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel
import os

app = FastAPI(title="Mohaj AI Research Assistant")

# CORS and middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchQuery(BaseModel):
    query: str
    search_n: int = 10
    search_provider: str = "google"
    is_reranking: bool = True
    is_detail: bool = True
    detail_min_score: float = 0.7
    detail_top_k: int = 3
    filters: Optional[dict] = None 