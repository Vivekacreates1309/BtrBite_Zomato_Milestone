import { useState } from 'react';
import './RestaurantCard.css';

/* Deterministic cuisine → Unsplash image mapping.
   Every entry has a UNIQUE Unsplash photo ID — no duplicates. */
const CUISINE_IMAGES = {
  'italian':       'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=480&h=320&fit=crop&q=80',
  'chinese':       'https://images.unsplash.com/photo-1585032226651-759b368d7246?w=480&h=320&fit=crop&q=80',
  'north indian':  'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=480&h=320&fit=crop&q=80',
  'south indian':  'https://images.unsplash.com/photo-1630383249896-424e482df921?w=480&h=320&fit=crop&q=80',
  'biryani':       'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=480&h=320&fit=crop&q=80',
  'cafe':          'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=480&h=320&fit=crop&q=80',
  'bakery':        'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=480&h=320&fit=crop&q=80',
  'desserts':      'https://images.unsplash.com/photo-1551024506-0bccd828d307?w=480&h=320&fit=crop&q=80',
  'fast food':     'https://images.unsplash.com/photo-1561758033-d89a9ad46330?w=480&h=320&fit=crop&q=80',
  'street food':   'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=480&h=320&fit=crop&q=80',
  'pizza':         'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=480&h=320&fit=crop&q=80',
  'continental':   'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=480&h=320&fit=crop&q=80',
  'mexican':       'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=480&h=320&fit=crop&q=80',
  'japanese':      'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=480&h=320&fit=crop&q=80',
  'thai':          'https://images.unsplash.com/photo-1562565652-a0d8f0c59eb4?w=480&h=320&fit=crop&q=80',
  'seafood':       'https://images.unsplash.com/photo-1615141982883-c7ad0e69fd62?w=480&h=320&fit=crop&q=80',
  'mughlai':       'https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=480&h=320&fit=crop&q=80',
  'beverages':     'https://images.unsplash.com/photo-1544145945-f90425340c7e?w=480&h=320&fit=crop&q=80',
  'ice cream':     'https://images.unsplash.com/photo-1501443762994-82bd5dace89a?w=480&h=320&fit=crop&q=80',
  'pan-asian':     'https://images.unsplash.com/photo-1617093727343-374698b1b08d?w=480&h=320&fit=crop&q=80',
  'cocktails':     'https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=480&h=320&fit=crop&q=80',
  'fine dining':   'https://images.unsplash.com/photo-1550966871-3ed3cdb51f3a?w=480&h=320&fit=crop&q=80',
  'kebab':         'https://images.unsplash.com/photo-1603360946369-dc9bb6258143?w=480&h=320&fit=crop&q=80',
  'rolls':         'https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=480&h=320&fit=crop&q=80',
  'burger':        'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=480&h=320&fit=crop&q=80',
  'sandwich':      'https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=480&h=320&fit=crop&q=80',
  'salad':         'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=480&h=320&fit=crop&q=80',
  'korean':        'https://images.unsplash.com/photo-1590301157890-4810ed352733?w=480&h=320&fit=crop&q=80',
  'mediterranean': 'https://images.unsplash.com/photo-1544025162-d76694265947?w=480&h=320&fit=crop&q=80',
  'american':      'https://images.unsplash.com/photo-1550547660-d9450f859349?w=480&h=320&fit=crop&q=80',
  'momos':         'https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=480&h=320&fit=crop&q=80',
  'default':       'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=480&h=320&fit=crop&q=80',
};

function getImageForRestaurant(restaurant) {
  // Try to match the first cuisine that has a known image (exact match only)
  for (const cuisine of restaurant.cuisines) {
    const key = cuisine.toLowerCase().trim();
    if (CUISINE_IMAGES[key]) return CUISINE_IMAGES[key];
  }

  // Try partial match only if no exact cuisine matched (second pass)
  for (const cuisine of restaurant.cuisines) {
    const key = cuisine.toLowerCase().trim();
    for (const [imgKey, url] of Object.entries(CUISINE_IMAGES)) {
      if (imgKey !== 'default' && (key.includes(imgKey) || imgKey.includes(key))) {
        return url;
      }
    }
  }

  // Try rest_type match
  if (restaurant.rest_type) {
    const rt = restaurant.rest_type.toLowerCase();
    for (const [imgKey, url] of Object.entries(CUISINE_IMAGES)) {
      if (imgKey !== 'default' && rt.includes(imgKey)) return url;
    }
  }

  // Use a seeded hash based on name + location + id to maximize variety
  const fallbackKeys = Object.keys(CUISINE_IMAGES).filter(k => k !== 'default');
  const seed = `${restaurant.name}|${restaurant.location}|${restaurant.id}`;
  let hash = 0;
  for (let i = 0; i < seed.length; i++) {
    hash = ((hash << 5) - hash + seed.charCodeAt(i)) | 0;
  }
  const idx = Math.abs(hash) % fallbackKeys.length;
  return CUISINE_IMAGES[fallbackKeys[idx]];
}

export default function RestaurantCard({ restaurant, index }) {
  const delay = index * 100;
  const [imgError, setImgError] = useState(false);
  const imageUrl = getImageForRestaurant(restaurant);

  return (
    <article
      className="restaurant-card"
      style={{ animationDelay: `${delay}ms` }}
    >
      {/* Gradient border overlay */}
      <div className="card-border-glow" />

      {/* Hero image */}
      <div className="card-image-wrapper">
        {!imgError ? (
          <img
            className="card-image"
            src={imageUrl}
            alt={`${restaurant.name} restaurant`}
            loading="lazy"
            onError={() => setImgError(true)}
          />
        ) : (
          <div className="card-image-fallback">
            <span className="fallback-icon">🍽️</span>
          </div>
        )}
        <div className="card-image-overlay" />

        {/* Rank badge overlaid on image */}
        <div className="rank-badge">
          <span className="rank-number">#{restaurant.rank}</span>
          <span className="rank-label">Match</span>
        </div>

        {/* Rating badge on image */}
        <div className="image-rating-badge">
          <span className="star-icon">★</span>
          <span className="rating-num">{restaurant.rating.toFixed(1)}</span>
        </div>
      </div>

      {/* Content */}
      <div className="card-body">
        <h3 className="card-name headline-md">{restaurant.name}</h3>

        {/* Location + Cost subtitle */}
        <p className="card-subtitle">
          {restaurant.location} · ₹{restaurant.cost_for_two.toLocaleString('en-IN')} for two
        </p>

        {/* Cuisine chips */}
        <div className="cuisine-chips">
          {restaurant.cuisines.slice(0, 3).map((c) => (
            <span key={c} className="cuisine-chip">{c}</span>
          ))}
        </div>

        {/* AI Explanation */}
        <div className="ai-explanation">
          <span className="ai-icon">✨</span>
          <p className="ai-text">{restaurant.explanation}</p>
        </div>
      </div>
    </article>
  );
}
