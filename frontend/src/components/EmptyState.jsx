import './EmptyState.css';

export default function EmptyState() {
  return (
    <div className="empty-state">
      <div className="empty-icon">🍽️</div>
      <h3 className="headline-md">No restaurants found</h3>
      <p className="body-md empty-desc">
        We couldn't find any matches for your preferences. Try adjusting your filters — perhaps a different location, budget, or cuisine!
      </p>
    </div>
  );
}
