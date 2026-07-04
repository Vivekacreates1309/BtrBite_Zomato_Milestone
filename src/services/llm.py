import json
from typing import List, Dict
from groq import Groq
from ..models.restaurant import Restaurant
from ..models.preferences import UserPreferences
from ..config import settings

class PromptBuilder:
    SYSTEM_PROMPT = """You are an AI restaurant recommendation assistant.
Your task is to rank the provided list of restaurant candidates based on the user's preferences.
You must output a JSON object containing a 'recommendations' array.
Each item in the array must have:
- 'id': the ID of the restaurant.
- 'explanation': a personalized explanation (max 2 sentences) of why it's a good fit.
- 'rank': an integer ranking from 1 to N (1 being the best).

Do not output any markdown formatting, only valid JSON.
"""
    
    @staticmethod
    def build_messages(candidates: List[Restaurant], prefs: UserPreferences) -> List[Dict[str, str]]:
        candidates_json = [
            {
                "id": r.id,
                "name": r.name,
                "cuisines": r.cuisines,
                "rating": r.rating,
                "cost_for_two": r.cost_for_two
            } for r in candidates
        ]
        
        user_message = f"User Preferences:\nLocation: {prefs.location}\nBudget: {prefs.budget}\n"
        if prefs.cuisine:
            user_message += f"Cuisine: {prefs.cuisine}\n"
        if prefs.additional:
            user_message += f"Additional: {prefs.additional}\n"
        
        user_message += f"\nCandidates:\n{json.dumps(candidates_json, indent=2)}"
        
        return [
            {"role": "system", "content": PromptBuilder.SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ]

class LLMClient:
    def __init__(self):
        self.client = Groq(api_key=settings.groq_api_key) if settings.groq_api_key else None
        self.model = settings.groq_model
        
    def get_recommendations(self, candidates: List[Restaurant], prefs: UserPreferences) -> str:
        if not self.client:
            # Fallback if no API key is provided
            fallback = {
                "recommendations": [
                    {
                        "id": c.id, 
                        "explanation": "Fallback explanation since Groq API key is missing.", 
                        "rank": idx + 1
                    } for idx, c in enumerate(candidates)
                ]
            }
            return json.dumps(fallback)
            
        messages = PromptBuilder.build_messages(candidates, prefs)
        response = self.client.chat.completions.create(
            messages=messages,
            model=self.model,
            response_format={"type": "json_object"},
            temperature=settings.groq_temperature,
        )
        return response.choices[0].message.content
