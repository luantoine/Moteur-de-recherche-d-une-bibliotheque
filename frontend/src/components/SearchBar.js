import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import {LIMIT_BOOK_TOSHOW} from "../config/config";

const SearchBar = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const queryParam = queryParams.get("query");
    const [query, setQuery] = useState(queryParam || "");
    const [history, setHistory] = useState([]);

    useEffect(() => {
        const storedHistory = JSON.parse(localStorage.getItem("searchHistory")) || [];
        setHistory(storedHistory);
    }, []);

    const saveToHistory = (query) => {
        const newHistory = [query, ...history].slice(0, 10); // Limiter à 10 éléments
        setHistory(newHistory);
        localStorage.setItem("searchHistory", JSON.stringify(newHistory));
    };

    const searchOnclick = () => {
        if (query.trim() !== "") {
            saveToHistory(query);
            navigate(`/books?query=${encodeURIComponent(query)}&limit=${LIMIT_BOOK_TOSHOW}&offset=0`);
        } else {
            alert("Veuillez entrer une recherche valide.");
        }
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
                    placeholder={"Saissisez un mot ou une phrase"}
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


            {/* Historique des recherches */}
            Historique des recherches
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
                                    navigate(`/books?query=${encodeURIComponent(item)}&limit=${LIMIT_BOOK_TOSHOW}&offset=0`);
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
