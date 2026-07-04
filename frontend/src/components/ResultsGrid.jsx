import RestaurantCard from './RestaurantCard';
import './ResultsGrid.css';

export default function ResultsGrid({ results }) {
  return (
    <section className="results-section">
      <div className="results-header">
        <h2 className="headline-lg gradient-text">
          We found {results.length} perfect bite{results.length !== 1 ? 's' : ''} for you
        </h2>
        <p className="results-subtitle body-md">
          Ranked by our AI based on your preferences
        </p>
      </div>
      <div className="results-grid">
        {results.map((r, i) => (
          <RestaurantCard key={r.id} restaurant={r} index={i} />
        ))}
      </div>
    </section>
  );
}
