import React, { useState, useEffect } from 'react';
import './index.css';

const API_BASE = 'http://127.0.0.1:8000/api';

function formatAuthors(authors) {
    if (!authors || !Array.isArray(authors) || authors.length === 0) {
      return "Auteur inconnu";
    }
    const formatted = authors
      .map(a => {
         if (typeof a === 'string') return a;
         if (typeof a === 'object' && a.name) return a.name;
         return '';
      })
      .filter(author => author !== '')
      .join(', ');
    return formatted || "Auteur inconnu";
  }

function SearchComponent({ onSearchResult, onBookSelect }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [suggestions, setSuggestions] = useState([]);

  const handleSearch = async () => {
    if (!query) return;
    const cacheKey = `search:${query}`;
    const cached = localStorage.getItem(cacheKey);
    if (cached) {
      const data = JSON.parse(cached);
      setResults(data.results);
      setSuggestions(data.suggestions);
      onSearchResult('normal', query, data);
      return;
    }
    try {
      const response = await fetch(`${API_BASE}/search/?q=${encodeURIComponent(query)}`);
      const data = await response.json();
      if (response.ok) {
        setResults(data.results);
        setSuggestions(data.suggestions);
        try {
          localStorage.setItem(cacheKey, JSON.stringify(data));
        } catch(e) {
          console.error('Erreur lors de la mise en cache:', e);
        }
        onSearchResult('normal', query, data);
      } else {
        console.error(data.error);
      }
    } catch (error) {
      console.error("Erreur lors de la récupération des résultats :", error);
    }
  };

  return (
    <div>
      <h2>Recherche</h2>
      <input
        type="text"
        value={query}
        onChange={e => setQuery(e.target.value)}
        placeholder="Entrez un mot-clé"
      />
      <button onClick={handleSearch}>Chercher</button>

      <h3>Résultats :</h3>
      <ul>
        {results.map((book) => (
          <li
            key={book._id}
            onClick={() => onBookSelect(book)}
            style={{ cursor: 'pointer', display: 'flex', alignItems: 'center', marginBottom: '10px' }}
          >
            {book.cover_url && (
              <img src={book.cover_url} alt={book.title} className="book-cover" />
            )}
            <div>
              <strong>{book.title}</strong> par {formatAuthors(book.authors)} — Occurrences : {book.occurrences}, Centralité : {book.centrality}
            </div>
          </li>
        ))}
      </ul>

      <h3>Suggestions :</h3>
      <ul>
        {suggestions.map((book) => (
          <li
            key={book._id}
            onClick={() => onBookSelect(book)}
            style={{ cursor: 'pointer', display: 'flex', alignItems: 'center', marginBottom: '10px' }}
          >
            {book.cover_url && (
              <img src={book.cover_url} alt={book.title} className="book-cover" />
            )}
            <div>
              <strong>{book.title}</strong> par {formatAuthors(book.authors)}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

function AdvancedSearchComponent({ onSearchResult, onBookSelect }) {
  const [regex, setRegex] = useState('');
  const [results, setResults] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleAdvancedSearch = async () => {
    if (!regex) return;
    setLoading(true);
    const timer = setTimeout(() => setLoading(false), 10000); // 10 sec max
    const cacheKey = `advanced:${regex}`;
    const cached = localStorage.getItem(cacheKey);
    if (cached) {
      const data = JSON.parse(cached);
      setResults(data.results);
      setSuggestions(data.suggestions);
      onSearchResult('advanced', regex, data);
      setLoading(false);
      clearTimeout(timer);
      return;
    }
    try {
      const response = await fetch(`${API_BASE}/advanced_search/?regex=${encodeURIComponent(regex)}`);
      const data = await response.json();
      if (response.ok) {
        setResults(data.results);
        setSuggestions(data.suggestions);
        try {
          localStorage.setItem(cacheKey, JSON.stringify(data));
        } catch(e) {
          console.error('Erreur lors de la mise en cache:', e);
        }
        onSearchResult('advanced', regex, data);
      } else {
        console.error(data.error);
      }
    } catch (error) {
      console.error("Erreur lors de la recherche avancée :", error);
    } finally {
      setLoading(false);
      clearTimeout(timer);
    }
  };

  return (
    <div>
      <h2>Recherche Avancée</h2>
      <input
        type="text"
        value={regex}
        onChange={e => setRegex(e.target.value)}
        placeholder="Entrez une expression régulière"
      />
      <button
        onClick={handleAdvancedSearch}
        disabled={loading}
        style={{ opacity: loading ? 0.5 : 1 }}
      >
        {loading ? 'Chargement...' : 'Chercher Avancé'}
      </button>

      <h3>Résultats :</h3>
      <ul>
        {results.map((book) => (
          <li
            key={book._id}
            onClick={() => onBookSelect(book)}
            style={{ cursor: 'pointer', display: 'flex', alignItems: 'center', marginBottom: '10px' }}
          >
            {book.cover_url && (
              <img src={book.cover_url} alt={book.title} className="book-cover" />
            )}
            <div>
              <strong>{book.title}</strong> par {formatAuthors(book.authors)} — Occurrences : {book.occurrences}, Centralité : {book.centrality}
            </div>
          </li>
        ))}
      </ul>

      <h3>Suggestions :</h3>
      <ul>
        {suggestions.map((book) => (
          <li
            key={book._id}
            onClick={() => onBookSelect(book)}
            style={{ cursor: 'pointer', display: 'flex', alignItems: 'center', marginBottom: '10px' }}
          >
            {book.cover_url && (
              <img src={book.cover_url} alt={book.title} className="book-cover" />
            )}
            <div>
              <strong>{book.title}</strong> par {formatAuthors(book.authors)}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

function HistoryComponent({ history, onHistorySelect }) {
  return (
    <div>
      <h2>Historique des recherches</h2>
      <ul>
        {history.map((entry, index) => (
          <li key={index}>
            <button
              onClick={() => onHistorySelect(entry)}
              style={{
                background: 'none',
                border: 'none',
                padding: 0,
                textDecoration: 'underline',
                color: 'blue',
                cursor: 'pointer'
              }}
            >
              [{entry.type}] {entry.query}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

function BookDetailModal({ book, onClose }) {
  if (!book) return null;

  const handleReadBook = () => {
    if (book.text) {
      const newWindow = window.open('', '_blank');
      newWindow.document.write(`<pre>${book.text}</pre>`);
      newWindow.document.close();
    } else if (book.text_url) {
      window.open(book.text_url, '_blank');
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <button className="close-btn" onClick={onClose}>X</button>
        {book.cover_url && <img src={book.cover_url} alt={book.title} className="book-cover" />}
        <h2>{book.title}</h2>
        <p><strong>Auteurs:</strong> {formatAuthors(book.authors)}</p>
        {book.subjects && <p><strong>Sujets:</strong> {book.subjects.join(', ')}</p>}
        <p><strong>Centralité:</strong> {book.centrality}</p>
        <p><strong>Occurrences:</strong> {book.occurrences}</p>
        <button onClick={handleReadBook}>Lire le livre</button>
      </div>
    </div>
  );
}

function App() {
  const [tab, setTab] = useState('search'); // 'search' ou 'advanced'
  const [history, setHistory] = useState([]);
  const [selectedBook, setSelectedBook] = useState(null);

  useEffect(() => {
    const storedHistory = localStorage.getItem('search_history');
    if (storedHistory) {
      setHistory(JSON.parse(storedHistory));
    }
  }, []);

  const handleSearchResult = (type, query, data) => {
    const newEntry = { type, query, data };
    const newHistory = [newEntry, ...history].slice(0, 20);
    setHistory(newHistory);
    try {
      localStorage.setItem('search_history', JSON.stringify(newHistory));
    } catch(e) {
      console.error('Erreur lors de la mise en cache de l\'historique:', e);
    }
  };

  const handleHistorySelect = (entry) => {
    alert(`Recherche précédente sélectionnée : [${entry.type}] ${entry.query}`);
    // Possibilité de réafficher les résultats via entry.data si nécessaire
  };

  const handleBookSelect = (book) => setSelectedBook(book);
  const handleModalClose = () => setSelectedBook(null);

  return (
    <div>
      <header>
        <h1>Moteur de Recherche de Livres</h1>
        <nav>
          <button onClick={() => setTab('search')}>Recherche</button>
          <button onClick={() => setTab('advanced')}>Recherche Avancée</button>
        </nav>
      </header>
      <main>
        {tab === 'search' ? (
          <SearchComponent onSearchResult={handleSearchResult} onBookSelect={handleBookSelect} />
        ) : (
          <AdvancedSearchComponent onSearchResult={handleSearchResult} onBookSelect={handleBookSelect} />
        )}
        <HistoryComponent history={history} onHistorySelect={handleHistorySelect} />
        {selectedBook && <BookDetailModal book={selectedBook} onClose={handleModalClose} />}
      </main>
    </div>
  );
}

export default App;
