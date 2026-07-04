import json
from typing import List
from ..models.restaurant import Restaurant
from ..models.recommendation import LLMRecommendationResponse, LLMRecommendationItem, RecommendationResponse

class ResponseParser:
    @staticmethod
    def parse(llm_response: str) -> List[LLMRecommendationItem]:
        try:
            data = json.loads(llm_response)
            parsed = LLMRecommendationResponse(**data)
            return parsed.recommendations
        except Exception as e:
            print(f"Failed to parse LLM response: {e}")
            return []

class RecommendationEnricher:
    @staticmethod
    def enrich(candidates: List[Restaurant], llm_items: List[LLMRecommendationItem]) -> List[RecommendationResponse]:
        # Map candidates by ID
        candidate_map = {r.id: r for r in candidates}
        
        results = []
        for item in llm_items:
            restaurant = candidate_map.get(item.id)
            if restaurant:
                # Merge fields from restaurant and LLM item
                enriched = RecommendationResponse(
                    **restaurant.model_dump(),
                    explanation=item.explanation,
                    rank=item.rank
                )
                results.append(enriched)
                
        # Sort by rank ascending (1 is best)
        results.sort(key=lambda x: x.rank)
        return results
