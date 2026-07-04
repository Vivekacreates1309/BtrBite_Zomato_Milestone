import { useState, useEffect, useRef } from 'react';
import { fetchLocations, fetchCuisines } from '../api/client';
import './PreferenceForm.css';

export default function PreferenceForm({ onSubmit, isLoading }) {
  const [locations, setLocations] = useState([]);
  const [cuisines, setCuisines] = useState([]);
  const [location, setLocation] = useState('');
  const [locationSearch, setLocationSearch] = useState('');
  const [showLocationDropdown, setShowLocationDropdown] = useState(false);
  const [budget, setBudget] = useState('medium');
  const [cuisine, setCuisine] = useState('');
  const [cuisineSearch, setCuisineSearch] = useState('');
  const [showCuisineDropdown, setShowCuisineDropdown] = useState(false);
  const [minRating, setMinRating] = useState(3.5);
  const [additional, setAdditional] = useState('');

  const locationRef = useRef(null);
  const cuisineRef = useRef(null);

  useEffect(() => {
    fetchLocations().then(setLocations).catch(console.error);
    fetchCuisines().then(setCuisines).catch(console.error);
  }, []);

  // Close dropdowns on outside click
  useEffect(() => {
    function handleClick(e) {
      if (locationRef.current && !locationRef.current.contains(e.target)) {
        setShowLocationDropdown(false);
      }
      if (cuisineRef.current && !cuisineRef.current.contains(e.target)) {
        setShowCuisineDropdown(false);
      }
    }
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, []);

  const filteredLocations = locations.filter((l) =>
    l.toLowerCase().includes(locationSearch.toLowerCase())
  );

  const filteredCuisines = cuisines.filter((c) =>
    c.toLowerCase().includes(cuisineSearch.toLowerCase())
  );

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!location) return;

    const prefs = {
      location,
      budget,
      min_rating: minRating,
    };
    if (cuisine) prefs.cuisine = cuisine;
    if (additional.trim()) prefs.additional = additional.trim();

    onSubmit(prefs);
  };

  const renderStars = () => {
    const stars = [];
    for (let i = 1; i <= 5; i++) {
      const filled = i <= minRating;
      const half = !filled && i - 0.5 <= minRating;
      stars.push(
        <button
          key={i}
          type="button"
          className={`star-btn ${filled ? 'filled' : ''} ${half ? 'half' : ''}`}
          onClick={() => setMinRating(i === minRating ? i - 0.5 : i)}
          aria-label={`${i} stars`}
        >
          ★
        </button>
      );
    }
    return stars;
  };

  return (
    <form className="pref-form glass" onSubmit={handleSubmit}>
      <h2 className="pref-form-title headline-md">What are you craving?</h2>

      <div className="pref-form-grid">
        {/* Location */}
        <div className="form-group" ref={locationRef}>
          <label className="label-md">Location *</label>
          <div className="search-select">
            <input
              type="text"
              className="form-input"
              placeholder="Search locations..."
              value={showLocationDropdown ? locationSearch : location || locationSearch}
              onChange={(e) => {
                setLocationSearch(e.target.value);
                setLocation('');
                setShowLocationDropdown(true);
              }}
              onFocus={() => setShowLocationDropdown(true)}
            />
            {location && !showLocationDropdown && (
              <button
                type="button"
                className="clear-btn"
                onClick={() => { setLocation(''); setLocationSearch(''); }}
              >×</button>
            )}
            {showLocationDropdown && filteredLocations.length > 0 && (
              <ul className="dropdown-list">
                {filteredLocations.slice(0, 50).map((l) => (
                  <li
                    key={l}
                    className={`dropdown-item ${l === location ? 'active' : ''}`}
                    onClick={() => {
                      setLocation(l);
                      setLocationSearch('');
                      setShowLocationDropdown(false);
                    }}
                  >
                    {l}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>

        {/* Budget */}
        <div className="form-group">
          <label className="label-md">Budget <span className="optional">(for two)</span></label>
          <div className="budget-pills">
            {[
              { key: 'low',    icon: '💰', label: '₹300 – 500' },
              { key: 'medium', icon: '💳', label: '₹500 – 1,500' },
              { key: 'high',   icon: '💎', label: '₹1,500+' },
            ].map(({ key, icon, label }) => (
              <button
                key={key}
                type="button"
                className={`budget-pill ${budget === key ? 'active' : ''}`}
                onClick={() => setBudget(key)}
              >
                <span className="budget-icon">{icon}</span>
                <span className="budget-label">{label}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Cuisine */}
        <div className="form-group" ref={cuisineRef}>
          <label className="label-md">Cuisine <span className="optional">(optional)</span></label>
          <div className="search-select">
            <input
              type="text"
              className="form-input"
              placeholder="Any cuisine..."
              value={showCuisineDropdown ? cuisineSearch : cuisine || cuisineSearch}
              onChange={(e) => {
                setCuisineSearch(e.target.value);
                setCuisine('');
                setShowCuisineDropdown(true);
              }}
              onFocus={() => setShowCuisineDropdown(true)}
            />
            {cuisine && !showCuisineDropdown && (
              <button
                type="button"
                className="clear-btn"
                onClick={() => { setCuisine(''); setCuisineSearch(''); }}
              >×</button>
            )}
            {showCuisineDropdown && filteredCuisines.length > 0 && (
              <ul className="dropdown-list">
                {filteredCuisines.slice(0, 50).map((c) => (
                  <li
                    key={c}
                    className={`dropdown-item ${c === cuisine ? 'active' : ''}`}
                    onClick={() => {
                      setCuisine(c);
                      setCuisineSearch('');
                      setShowCuisineDropdown(false);
                    }}
                  >
                    {c}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>

        {/* Rating */}
        <div className="form-group">
          <label className="label-md">Minimum Rating</label>
          <div className="rating-control">
            <div className="stars-row">{renderStars()}</div>
            <span className="rating-value">{minRating.toFixed(1)}</span>
          </div>
        </div>
      </div>

      {/* Additional */}
      <div className="form-group form-group-full">
        <label className="label-md">Additional Preferences <span className="optional">(optional)</span></label>
        <textarea
          className="form-textarea"
          placeholder="e.g., family-friendly, outdoor seating, quick service..."
          value={additional}
          onChange={(e) => setAdditional(e.target.value)}
          rows={2}
        />
      </div>

      {/* Submit */}
      <button
        type="submit"
        className="submit-btn"
        disabled={!location || isLoading}
      >
        {isLoading ? (
          <span className="btn-loading">
            <span className="spinner" />
            Curating...
          </span>
        ) : (
          <span>Find My Bite ✨</span>
        )}
      </button>
    </form>
  );
}
