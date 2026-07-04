from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from ..models.preferences import UserPreferences
from ..models.restaurant import Restaurant
from ..models.recommendation import RecommendationResponse
from ..data.repository import RestaurantRepository
from ..services.validation import PreferenceNormalizer, PreferenceValidator
from ..services.filtering import CandidateSelector
from ..services.llm import LLMClient
from ..services.enrichment import ResponseParser, RecommendationEnricher

app = FastAPI(title="BtrBite AI Recommendation API", version="1.0.0")

# CORS — allow React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the repository and LLM Client on startup
repository = RestaurantRepository()
llm_client = LLMClient()

# Cache for dropdown values (computed once on first request)
_locations_cache: List[str] = []
_cuisines_cache: List[str] = []

def _build_dropdown_caches():
    global _locations_cache, _cuisines_cache
    if _locations_cache and _cuisines_cache:
        return
    all_restaurants = repository.get_all()
    _locations_cache = sorted(set(r.location for r in all_restaurants if r.location))
    cuisine_set = set()
    for r in all_restaurants:
        for c in r.cuisines:
            if c.strip():
                cuisine_set.add(c.strip())
    _cuisines_cache = sorted(cuisine_set)

@app.get("/health")
def health_check():
    return {"status": "healthy", "restaurants_loaded": len(repository.get_all())}

@app.get("/api/v1/locations", response_model=List[str])
def get_locations():
    _build_dropdown_caches()
    return _locations_cache

@app.get("/api/v1/cuisines", response_model=List[str])
def get_cuisines():
    _build_dropdown_caches()
    return _cuisines_cache

@app.post("/api/v1/recommend", response_model=List[RecommendationResponse])
def recommend_restaurants(prefs: UserPreferences):
    try:
        # 1. Normalize and validate preferences
        normalized_prefs = PreferenceNormalizer.normalize(prefs)
        PreferenceValidator.validate(normalized_prefs)
        
        # 2. Get all restaurants from the repository
        all_restaurants = repository.get_all()
        
        if not all_restaurants:
            print("WARNING: Repository is empty — no restaurants loaded.")
            return []
        
        # 3. Filter and select candidates
        candidates = CandidateSelector.select(all_restaurants, normalized_prefs, limit=10)
        
        if not candidates:
            print(f"No candidates found for prefs: location={normalized_prefs.location}, "
                  f"budget={normalized_prefs.budget}, cuisine={normalized_prefs.cuisine}, "
                  f"min_rating={normalized_prefs.min_rating}")
            return []
            
        # 4. Get LLM recommendations
        try:
            llm_response_str = llm_client.get_recommendations(candidates, normalized_prefs)
            
            # 5. Parse and enrich
            llm_items = ResponseParser.parse(llm_response_str)
            enriched_results = RecommendationEnricher.enrich(candidates, llm_items)
        except Exception as llm_err:
            print(f"LLM recommendation failed: {llm_err}")
            enriched_results = []
        
        # Fallback to candidates if LLM failed
        if not enriched_results:
            # We can convert raw candidates to RecommendationResponse manually
            fallback = [
                RecommendationResponse(
                    **c.model_dump(),
                    explanation="Recommended based on your location, budget, and rating preferences.",
                    rank=idx + 1
                ) for idx, c in enumerate(candidates)
            ]
            return fallback
            
        return enriched_results
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Unexpected error in recommend_restaurants: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

