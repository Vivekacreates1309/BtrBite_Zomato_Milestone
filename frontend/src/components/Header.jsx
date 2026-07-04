import './Header.css';

export default function Header() {
  return (
    <header className="header">
      <div className="header-inner">
        <div className="header-brand">
          <span className="header-sparkle">✨</span>
          <h1 className="header-logo gradient-text headline-xl">BtrBite</h1>
        </div>
        <p className="header-tagline body-md">AI-Powered Restaurant Recommendations</p>
      </div>
    </header>
  );
}
