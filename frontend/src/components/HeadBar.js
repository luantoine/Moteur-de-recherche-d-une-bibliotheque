import React from 'react';
import SearchBar from "./SearchBar";

const HeadBar = () => {
    return (
        <header
            style={{
                display: "flex",
                flexDirection: "column", // Permet d'empiler les éléments
                alignItems: "center", // Centre horizontalement les éléments
                justifyContent: "center", // Centre verticalement
                padding: "20px",
                backgroundColor: "#4CAF50",
                color: "#fff",
                boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
            }}
        >
            <h1
                style={{
                    fontSize: "28px",
                    fontWeight: "bold",
                    margin: "0",
                    marginBottom: "10px", // Espace entre le titre et la barre de recherche
                }}
            >
                Databerg
            </h1>
            <SearchBar />
        </header>
    );
};

export default HeadBar;
