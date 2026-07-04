import './LoadingState.css';

export default function LoadingState() {
  return (
    <section className="loading-section">
      <p className="loading-text body-lg">
        <span className="loading-sparkle">✨</span>
        Our AI is curating your perfect bites...
      </p>
      <div className="skeleton-grid">
        {[0, 1, 2].map((i) => (
          <div key={i} className="skeleton-card" style={{ animationDelay: `${i * 150}ms` }}>
            <div className="skel skel-badge" />
            <div className="skel skel-title" />
            <div className="skel-chips">
              <div className="skel skel-chip" />
              <div className="skel skel-chip short" />
            </div>
            <div className="skel skel-meta" />
            <div className="skel skel-explanation" />
            <div className="skel skel-explanation short" />
          </div>
        ))}
      </div>
    </section>
  );
}
