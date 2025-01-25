import React, {useState} from 'react';
import {useLocation, useNavigate} from "react-router-dom";


const SearchBar = () => {
    const [searchType, setSearchType] = useState("simple");
    const navigate = useNavigate();
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const queryParam = queryParams.get("query");
    const [query, setQuery] = useState(queryParam);

    // Définir un placeholder en fonction de searchType
    const getPlaceholder = () => {
        switch (searchType) {
            case 'simple':
                return "Entrez un mot-clé pour une recherche simple";
            case 'advanced':
                return "Entrez un mot/phrase/regex pour une recherche avancée";
            default:
                return "Entrez un mot-clé pour une recherche simple";
        }
    };

    function searchOnclick(query) {
        if (query.trim() !== "") {
            navigate(`/books?query=${encodeURIComponent(query)}&type=${encodeURIComponent(searchType)}`);
        } else {
            alert("Veuillez entrer une recherche.");
        }
    }

    return (
        <div className={"container"}>
            <div className={"searchBar"}>
                <input
                    type="text"
                    className={"searchInput"}
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder={getPlaceholder()}
                />
                <button
                    className={"searchButton"}
                    onClick={() => searchOnclick(query)}
                > Chercher </button>
            </div>

            <nav>
                <button
                    className={searchType==="simple" ? "searchChoosed" : ""}
                    onClick={() => setSearchType('simple')}>Recherche Simple</button>
                <button
                    className={searchType==="advanced" ? "searchChoosed" : ""}
                    onClick={() => setSearchType('advanced')}>Recherche Avancée</button>
            </nav>
        </div>
    );
};

export default SearchBar;