import pytest
from src.models.restaurant import Restaurant
from src.models.preferences import UserPreferences
from src.services.filtering import CandidateSelector, RestaurantFilter
from src.services.validation import PreferenceNormalizer, PreferenceValidator

@pytest.fixture
def mock_restaurants():
    return [
        Restaurant(
            id="1", name="Cheap Bites", location="New York", cuisines=["Fast Food", "American"],
            cost_for_two=10, rating=3.5, votes=100, budget_tier="low"
        ),
        Restaurant(
            id="2", name="Fancy Italian", location="New York", cuisines=["Italian"],
            cost_for_two=100, rating=4.8, votes=500, budget_tier="high"
        ),
        Restaurant(
            id="3", name="Average Diner", location="New York", cuisines=["American", "Diner"],
            cost_for_two=30, rating=4.0, votes=300, budget_tier="medium"
        ),
        Restaurant(
            id="4", name="Sushi Place", location="San Francisco", cuisines=["Japanese", "Sushi"],
            cost_for_two=80, rating=4.5, votes=200, budget_tier="high"
        )
    ]

def test_filter_by_location(mock_restaurants):
    filtered = RestaurantFilter.filter_by_location(mock_restaurants, "New York")
    assert len(filtered) == 3
    assert all(r.location == "New York" for r in filtered)

def test_filter_by_budget(mock_restaurants):
    filtered = RestaurantFilter.filter_by_budget(mock_restaurants, "medium")
    assert len(filtered) == 1
    assert filtered[0].name == "Average Diner"

def test_filter_by_rating(mock_restaurants):
    filtered = RestaurantFilter.filter_by_rating(mock_restaurants, 4.2)
    assert len(filtered) == 2
    assert all(r.rating >= 4.2 for r in filtered)

def test_filter_by_cuisine(mock_restaurants):
    filtered = RestaurantFilter.filter_by_cuisine(mock_restaurants, "italian")
    assert len(filtered) == 1
    assert filtered[0].name == "Fancy Italian"

def test_candidate_selector(mock_restaurants):
    prefs = UserPreferences(location="New York", budget="high", min_rating=4.0, cuisine="italian")
    
    normalized = PreferenceNormalizer.normalize(prefs)
    PreferenceValidator.validate(normalized)
    
    candidates = CandidateSelector.select(mock_restaurants, normalized)
    
    assert len(candidates) == 1
    assert candidates[0].name == "Fancy Italian"

def test_candidate_selector_no_cuisine(mock_restaurants):
    prefs = UserPreferences(location="New York", budget="low", min_rating=3.0)
    
    normalized = PreferenceNormalizer.normalize(prefs)
    PreferenceValidator.validate(normalized)
    
    candidates = CandidateSelector.select(mock_restaurants, normalized)
    
    assert len(candidates) == 1
    assert candidates[0].name == "Cheap Bites"

def test_validation_errors():
    with pytest.raises(ValueError):
        prefs = UserPreferences(location="", budget="low")
        PreferenceValidator.validate(prefs)
        
    with pytest.raises(ValueError):
        prefs = UserPreferences(location="NY", budget="invalid_budget")
        PreferenceValidator.validate(prefs)
        
    with pytest.raises(ValueError):
        prefs = UserPreferences(location="NY", budget="low", min_rating=6.0)
        PreferenceValidator.validate(prefs)
