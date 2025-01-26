import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

const SearchBar = () => {
    const [searchType, setSearchType] = useState("simple");
    const navigate = useNavigate();
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const queryParam = queryParams.get("query");
    const [query, setQuery] = useState(queryParam || "");

    const getPlaceholder = () => {
        return searchType === "simple"
            ? "Entrez un mot-clé pour une recherche simple"
            : "Entrez un mot/phrase/regex pour une recherche avancée";
    };

    function searchOnclick() {
        if (query.trim() !== "") {
            navigate(`/books?query=${encodeURIComponent(query)}&limit=10&offset=0&type=${encodeURIComponent(searchType)}`);
        } else {
            alert("Veuillez entrer une recherche.");
        }
    }

    return (
        <div
            style={{
                display: "flex",
                flexDirection: "column",
                gap: "10px",
                alignItems: "center", // Centrer horizontalement
                justifyContent: "center", // Centrer verticalement
            }}
        >
            <div
                style={{
                    display: "flex",
                    gap: "10px",
                    width: "100%",
                    maxWidth: "600px", // Limite la largeur maximale
                }}
            >
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder={getPlaceholder()}
                    className={"searchInput"}
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
            <div
                style={{
                    display: "flex",
                    gap: "10px",
                    width: "100%",
                    maxWidth: "600px", // Alignement des boutons avec la barre
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
        </div>
    );
};

export default SearchBar;
