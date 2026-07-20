const API_BASE = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL}/api/v1`
  : '/api/v1';

export async function fetchLocations() {
  const res = await fetch(`${API_BASE}/locations`);
  if (!res.ok) throw new Error('Failed to fetch locations');
  return res.json();
}

export async function fetchCuisines() {
  const res = await fetch(`${API_BASE}/cuisines`);
  if (!res.ok) throw new Error('Failed to fetch cuisines');
  return res.json();
}

export async function getRecommendations(preferences) {
  const res = await fetch(`${API_BASE}/recommend`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(preferences),
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: 'Something went wrong. Please try again.' }));
    throw new Error(errorData.detail || `Request failed with status ${res.status}`);
  }

  return res.json();
}
