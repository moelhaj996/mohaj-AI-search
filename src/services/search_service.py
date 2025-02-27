from typing import List, Dict
import aiohttp
from components.embeddings import EmbeddingManager
from components.reranker import Reranker

class SearchService:
    def __init__(self, config: Dict):
        self.config = config
        self.embedding_manager = EmbeddingManager(
            model_name=config["OPENAI_EMBED_MODEL"],
            api_key=config["OPENAI_API_KEY"]
        )
        self.reranker = Reranker()

    async def search(self, query: SearchQuery) -> Dict:
        # Get initial search results
        raw_results = await self._fetch_search_results(query)
        
        if query.is_reranking:
            # Generate embeddings for query and results
            query_embedding = await self.embedding_manager.get_embedding(query.query)
            results = await self.reranker.rerank(
                raw_results,
                query_embedding,
                min_score=query.detail_min_score,
                top_k=query.detail_top_k
            )
        
        return {
            "results": results,
            "metadata": {
                "total_results": len(results),
                "reranked": query.is_reranking
            }
        } 