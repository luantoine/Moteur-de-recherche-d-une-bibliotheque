import React, { useState } from 'react';

function App() {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);

    const handleSearch = async () => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/api/search/?query=${query}`);
            const data = await response.json();
            setResults(data.results);
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    };

    return (
        <div>
            <h1>Library Search Engine</h1>
            <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Enter a keyword"
            />
            <button onClick={handleSearch}>Search</button>
            <ul>
                {results.map((result, index) => (
                    <li key={index}>{result}</li>
                ))}
            </ul>
        </div>
    );
}

export default App;
