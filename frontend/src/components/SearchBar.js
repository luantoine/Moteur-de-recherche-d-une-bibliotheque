import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";

const SearchBar = () => {
    const [searchType, setSearchType] = useState("simple");
    const navigate = useNavigate();
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const queryParam = queryParams.get("query");
    const [query, setQuery] = useState(queryParam || "");
    const [history, setHistory] = useState([]);

    // Charger l'historique depuis le Local Storage au chargement du composant
    useEffect(() => {
        const storedHistory = JSON.parse(localStorage.getItem("searchHistory")) || [];
        setHistory(storedHistory);
    }, []);

    // Enregistrer une recherche dans l'historique
    const saveToHistory = (query) => {
        const newHistory = [query, ...history].slice(0, 10); // Limiter à 10 éléments
        setHistory(newHistory);
        localStorage.setItem("searchHistory", JSON.stringify(newHistory));
    };

    // Gestion de la recherche
    const searchOnclick = () => {
        if (query.trim() !== "") {
            saveToHistory(query);
            navigate(`/books?query=${encodeURIComponent(query)}&limit=10&offset=0&type=${encodeURIComponent(searchType)}`);
        } else {
            alert("Veuillez entrer une recherche valide.");
        }
    };

    const getPlaceholder = () => {
        return searchType === "simple"
            ? "Entrez un mot-clé pour une recherche simple"
            : "Entrez un mot/phrase/regex pour une recherche avancée";
    };

    return (
        <div
            style={{
                display: "flex",
                flexDirection: "column",
                gap: "20px",
                alignItems: "center",
                justifyContent: "center",
            }}
        >
            {/* Barre de recherche */}
            <div
                style={{
                    display: "flex",
                    gap: "10px",
                    width: "100%",
                    maxWidth: "600px",
                }}
            >
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder={getPlaceholder()}
                    className="searchInput"
                    style={{
                        flex: 1,
                        padding: "10px",
                        borderRadius: "5px",
                        border: "1px solid #ddd",
                        fontSize: "16px",
                    }}
                />
                <button
                    onClick={searchOnclick}
                    style={{
                        padding: "10px 20px",
                        border: "none",
                        borderRadius: "5px",
                        backgroundColor: "#4CAF50",
                        color: "#fff",
                        fontSize: "16px",
                        cursor: "pointer",
                    }}
                >
                    Chercher
                </button>
            </div>

            {/* Boutons pour le type de recherche */}
            <div
                style={{
                    display: "flex",
                    gap: "10px",
                    width: "100%",
                    maxWidth: "600px",
                }}
            >
                <button
                    onClick={() => setSearchType("simple")}
                    style={{
                        flex: 1,
                        padding: "10px",
                        backgroundColor: searchType === "simple" ? "#4CAF50" : "#fff",
                        color: searchType === "simple" ? "#fff" : "#333",
                        border: "1px solid #ddd",
                        borderRadius: "5px",
                        cursor: "pointer",
                    }}
                >
                    Recherche Simple
                </button>
                <button
                    onClick={() => setSearchType("advanced")}
                    style={{
                        flex: 1,
                        padding: "10px",
                        backgroundColor: searchType === "advanced" ? "#4CAF50" : "#fff",
                        color: searchType === "advanced" ? "#fff" : "#333",
                        border: "1px solid #ddd",
                        borderRadius: "5px",
                        cursor: "pointer",
                    }}
                >
                    Recherche Avancée
                </button>
            </div>

            {/* Historique des recherches */}
            {history.length > 0 && (
                <div
                    style={{
                        width: "100%",
                        maxWidth: "600px",
                        backgroundColor: "#f9f9f9",
                        padding: "10px",
                        borderRadius: "5px",
                        border: "1px solid #ddd",
                    }}
                >
                    <h3 style={{ margin: "0 0 10px", fontSize: "18px" }}>Historique des recherches</h3>
                    <ul style={{ margin: 0, padding: 0, listStyleType: "none" }}>
                        {history.map((item, index) => (
                            <li
                                key={index}
                                style={{
                                    padding: "8px 0",
                                    borderBottom: "1px solid #eee",
                                    cursor: "pointer",
                                    color: "#4CAF50",
                                }}
                                onClick={() => {
                                    setQuery(item);
                                    navigate(`/books?query=${encodeURIComponent(item)}&limit=10&offset=0&type=${encodeURIComponent(searchType)}`);
                                }}
                            >
                                {item}
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default SearchBar;
