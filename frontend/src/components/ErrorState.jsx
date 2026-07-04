import './ErrorState.css';

export default function ErrorState({ message, onRetry }) {
  return (
    <div className="error-state">
      <div className="error-icon">⚠️</div>
      <h3 className="headline-md">Something went wrong</h3>
      <p className="body-md error-desc">{message}</p>
      {onRetry && (
        <button className="retry-btn" onClick={onRetry}>
          Try Again
        </button>
      )}
    </div>
  );
}
