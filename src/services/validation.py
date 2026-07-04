from ..models.preferences import UserPreferences

class PreferenceNormalizer:
    @staticmethod
    def normalize(prefs: UserPreferences) -> UserPreferences:
        """
        Normalizes user preferences, handling lowercase formatting and aliases.
        """
        # location and budget are required, so they will always be strings
        prefs.location = prefs.location.strip().lower()
        prefs.budget = prefs.budget.strip().lower()
        
        if prefs.cuisine:
            prefs.cuisine = prefs.cuisine.strip().lower()
            
        if prefs.additional:
            prefs.additional = prefs.additional.strip()
            
        return prefs

class PreferenceValidator:
    VALID_BUDGETS = {"low", "medium", "high"}

    @classmethod
    def validate(cls, prefs: UserPreferences) -> None:
        """
        Validates the user preferences against business constraints.
        Raises ValueError if invalid.
        """
        if not prefs.location:
            raise ValueError("Location cannot be empty.")
            
        if prefs.budget not in cls.VALID_BUDGETS:
            raise ValueError(f"Invalid budget tier: '{prefs.budget}'. Must be one of {cls.VALID_BUDGETS}.")
            
        if prefs.min_rating < 0.0 or prefs.min_rating > 5.0:
            raise ValueError(f"Minimum rating must be between 0 and 5. Got: {prefs.min_rating}")
