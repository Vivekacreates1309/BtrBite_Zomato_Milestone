from typing import List
from ..models.restaurant import Restaurant
from ..models.preferences import UserPreferences

class RestaurantFilter:
    @staticmethod
    def filter_by_location(restaurants: List[Restaurant], location: str) -> List[Restaurant]:
        if not location:
            return restaurants
        target = location.lower().strip()
        # Exact match first (case-insensitive) — dropdown values come from the data
        exact = [r for r in restaurants if r.location.lower().strip() == target]
        if exact:
            return exact
        # Fallback to substring match for manual/typed entries
        return [r for r in restaurants if target in r.location.lower()]

    @staticmethod
    def filter_by_budget(restaurants: List[Restaurant], budget: str) -> List[Restaurant]:
        if not budget:
            return restaurants
        target = budget.lower()
        return [r for r in restaurants if r.budget_tier.lower() == target]

    @staticmethod
    def filter_by_budget_relaxed(restaurants: List[Restaurant], budget: str) -> List[Restaurant]:
        """Allow the selected tier AND one adjacent tier."""
        if not budget:
            return restaurants
        target = budget.lower()
        adjacent = {
            'low': {'low', 'medium'},
            'medium': {'low', 'medium', 'high'},
            'high': {'medium', 'high'},
        }
        allowed = adjacent.get(target, {target})
        return [r for r in restaurants if r.budget_tier.lower() in allowed]

    @staticmethod
    def filter_by_rating(restaurants: List[Restaurant], min_rating: float) -> List[Restaurant]:
        if min_rating <= 0:
            return restaurants
        return [r for r in restaurants if r.rating >= min_rating]

    @staticmethod
    def filter_by_cuisine(restaurants: List[Restaurant], cuisine: str) -> List[Restaurant]:
        if not cuisine:
            return restaurants
        target = cuisine.lower()
        return [r for r in restaurants if any(target in c.lower() for c in r.cuisines)]

class CandidateSelector:
    @classmethod
    def select(cls, restaurants: List[Restaurant], prefs: UserPreferences, limit: int = 10) -> List[Restaurant]:
        """
        Progressive filtering: starts strict, then relaxes filters one by one
        (cuisine → budget → rating) until we have enough candidates.
        This ensures we almost always return results when a location exists.
        """
        MIN_CANDIDATES = 3  # Minimum acceptable result count before relaxing

        # 1. Location filter (always required — this is the hard filter)
        candidates = RestaurantFilter.filter_by_location(restaurants, prefs.location)

        if not candidates:
            return []

        # 2. Try the strict path first: budget + rating + cuisine
        result = cls._apply_filters(candidates, prefs, strict_budget=True)

        if len(result) >= MIN_CANDIDATES:
            result.sort(key=lambda r: (r.rating, r.votes), reverse=True)
            return result[:limit]

        # 3. Relax cuisine filter (drop it)
        result = cls._apply_filters(candidates, prefs, strict_budget=True, skip_cuisine=True)

        if len(result) >= MIN_CANDIDATES:
            result.sort(key=lambda r: (r.rating, r.votes), reverse=True)
            return result[:limit]

        # 4. Relax budget filter (allow adjacent tiers)
        result = cls._apply_filters(candidates, prefs, strict_budget=False)

        if len(result) >= MIN_CANDIDATES:
            result.sort(key=lambda r: (r.rating, r.votes), reverse=True)
            return result[:limit]

        # 5. Relax budget + cuisine
        result = cls._apply_filters(candidates, prefs, strict_budget=False, skip_cuisine=True)

        if len(result) >= MIN_CANDIDATES:
            result.sort(key=lambda r: (r.rating, r.votes), reverse=True)
            return result[:limit]

        # 6. Drop rating entirely, keep relaxed budget
        result = RestaurantFilter.filter_by_budget_relaxed(candidates, prefs.budget)

        if len(result) >= MIN_CANDIDATES:
            result.sort(key=lambda r: (r.rating, r.votes), reverse=True)
            return result[:limit]

        # 7. Drop rating + budget entirely (just location + cuisine if set)
        if prefs.cuisine:
            result = RestaurantFilter.filter_by_cuisine(candidates, prefs.cuisine)
            if len(result) >= MIN_CANDIDATES:
                result.sort(key=lambda r: (r.rating, r.votes), reverse=True)
                return result[:limit]

        # 8. Final fallback: just location, sorted by relevance
        candidates.sort(key=lambda r: (r.rating, r.votes), reverse=True)
        return candidates[:limit]

    @classmethod
    def _apply_filters(
        cls,
        candidates: List[Restaurant],
        prefs: UserPreferences,
        strict_budget: bool = True,
        skip_cuisine: bool = False,
    ) -> List[Restaurant]:
        """Apply budget, rating, and optionally cuisine filters."""
        # Budget
        if strict_budget:
            filtered = RestaurantFilter.filter_by_budget(candidates, prefs.budget)
        else:
            filtered = RestaurantFilter.filter_by_budget_relaxed(candidates, prefs.budget)

        # Rating
        filtered = RestaurantFilter.filter_by_rating(filtered, prefs.min_rating)

        # Cuisine (optional)
        if not skip_cuisine and prefs.cuisine:
            filtered = RestaurantFilter.filter_by_cuisine(filtered, prefs.cuisine)

        return filtered

