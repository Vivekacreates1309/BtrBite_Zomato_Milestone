import { useState } from 'react';
import { getRecommendations } from './api/client';
import Header from './components/Header';
import PreferenceForm from './components/PreferenceForm';
import LoadingState from './components/LoadingState';
import ResultsGrid from './components/ResultsGrid';
import EmptyState from './components/EmptyState';
import ErrorState from './components/ErrorState';
import Footer from './components/Footer';
import './App.css';

export default function App() {
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [lastPrefs, setLastPrefs] = useState(null);

  const handleSubmit = async (prefs) => {
    setIsLoading(true);
    setError(null);
    setResults(null);
    setLastPrefs(prefs);

    try {
      const data = await getRecommendations(prefs);
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRetry = () => {
    if (lastPrefs) handleSubmit(lastPrefs);
  };

  return (
    <>
      <Header />

      <main className="main-content">
        <PreferenceForm onSubmit={handleSubmit} isLoading={isLoading} />

        {isLoading && <LoadingState />}

        {error && <ErrorState message={error} onRetry={handleRetry} />}

        {results && results.length > 0 && <ResultsGrid results={results} />}

        {results && results.length === 0 && <EmptyState />}
      </main>

      <Footer />
    </>
  );
}
