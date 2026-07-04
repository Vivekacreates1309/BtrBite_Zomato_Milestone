import json
from src.models.restaurant import Restaurant
from src.models.preferences import UserPreferences
from src.services.llm import PromptBuilder, LLMClient
from src.services.enrichment import ResponseParser, RecommendationEnricher

def test_prompt_builder():
    candidates = [
        Restaurant(
            id="1", name="Cheap Bites", location="New York", cuisines=["Fast Food"],
            cost_for_two=10, rating=3.5, votes=100, budget_tier="low"
        )
    ]
    prefs = UserPreferences(location="New York", budget="low")
    
    messages = PromptBuilder.build_messages(candidates, prefs)
    
    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"
    assert "New York" in messages[1]["content"]
    assert "Cheap Bites" in messages[1]["content"]

def test_response_parser_valid():
    llm_json = json.dumps({
        "recommendations": [
            {
                "id": "1",
                "explanation": "Great choice.",
                "rank": 1
            }
        ]
    })
    
    items = ResponseParser.parse(llm_json)
    assert len(items) == 1
    assert items[0].id == "1"
    assert items[0].rank == 1
    assert items[0].explanation == "Great choice."

def test_response_parser_invalid():
    # Should safely return empty list on parsing failure
    items = ResponseParser.parse("Invalid JSON string")
    assert items == []

def test_recommendation_enricher():
    candidates = [
        Restaurant(
            id="1", name="Cheap Bites", location="New York", cuisines=["Fast Food"],
            cost_for_two=10, rating=3.5, votes=100, budget_tier="low"
        )
    ]
    
    llm_json = json.dumps({
        "recommendations": [
            {
                "id": "1",
                "explanation": "Because it is cheap.",
                "rank": 1
            }
        ]
    })
    
    items = ResponseParser.parse(llm_json)
    enriched = RecommendationEnricher.enrich(candidates, items)
    
    assert len(enriched) == 1
    assert enriched[0].id == "1"
    assert enriched[0].name == "Cheap Bites"
    assert enriched[0].explanation == "Because it is cheap."
    assert enriched[0].rank == 1

def test_llm_client_fallback():
    # When api key is missing, we expect a fallback response
    client = LLMClient()
    candidates = [
        Restaurant(
            id="1", name="Cheap Bites", location="New York", cuisines=["Fast Food"],
            cost_for_two=10, rating=3.5, votes=100, budget_tier="low"
        )
    ]
    prefs = UserPreferences(location="New York", budget="low")
    
    # ensure fallback triggers (groq client shouldn't be initialized if .env is missing or empty)
    if not client.client:
        response_str = client.get_recommendations(candidates, prefs)
        items = ResponseParser.parse(response_str)
        assert len(items) == 1
        assert "fallback" in items[0].explanation.lower()
