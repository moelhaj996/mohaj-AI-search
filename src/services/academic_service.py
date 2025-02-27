from typing import List, Dict
import asyncio
from components.connectors import ArxivConnector, PubMedConnector, ScholarConnector

class AcademicService:
    def __init__(self):
        self.connectors = {
            "arxiv": ArxivConnector(),
            "pubmed": PubMedConnector(),
            "scholar": ScholarConnector()
        }
    
    async def search_academic(self, query: str, filters: Dict) -> List[Dict]:
        tasks = []
        for source, connector in self.connectors.items():
            if filters.get(source, True):  # Enable/disable specific sources
                tasks.append(connector.search(query, filters))
        
        results = await asyncio.gather(*tasks)
        return self._merge_and_deduplicate(results) 