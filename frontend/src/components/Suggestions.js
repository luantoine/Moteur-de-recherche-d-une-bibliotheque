import React, { useEffect, useState } from "react";
import getBooksByIds from "../config/getBooksById";
import BookSuggestion from "./BookSuggestion";

const Suggestions = ({ booksId }) => {
    const [currentIndex, setCurrentIndex] = useState(0);
    const [books, setBooks] = useState([]);
    const [onError,setOnError] = useState(null)

    const handlePrev = () => {
        setCurrentIndex((prevIndex) => Math.max(prevIndex - 1, 0));
    };

    const handleNext = () => {
        setCurrentIndex((prevIndex) => Math.min(prevIndex + 1, books.length - 1));
    };

    useEffect(() => {
        getBooksByIds(booksId)
            .then((data) => {
                setBooks(data);
                setOnError(null)
            })
            .catch((error) => {
                setOnError("Une erreur est survenue lors du chargement des suggestions.");
                console.error(error);
            });
    }, [booksId]);

    return (
        <div style={{ marginTop: "20px" }}>
            <h3 style={{ textAlign: "center", marginBottom: "10px" }}>
                Suggestions de livres
            </h3>
            <div
                style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    gap: "10px",
                }}
            >
                {/* Bouton précédent */}
                <button
                    onClick={handlePrev}
                    disabled={currentIndex === 0}
                    style={{
                        border: "none",
                        backgroundColor: "#4CAF50",
                        color: "#fff",
                        padding: "10px",
                        borderRadius: "5px",
                        cursor: currentIndex === 0 ? "not-allowed" : "pointer",
                        opacity: currentIndex === 0 ? 0.5 : 1,
                        transition: "opacity 0.3s",
                    }}
                >
                    ←
                </button>

                {/* Conteneur des livres */}
                <div
                    style={{
                        display: "flex",
                        overflow: "hidden", // Cache les livres en dehors de la zone visible
                        width: "300px", // Largeur visible du carrousel
                        position: "relative",
                    }}
                >
                    <div
                        style={{
                            display: "flex",
                            transform: `translateX(-${currentIndex * 310}px)`, // 300px correspond à la largeur visible
                            transition: "transform 0.3s ease-in-out",
                            gap: "10px",
                        }}
                    >
                        {books.map((book, index) => (
                            <div
                                key={book.id}
                                style={{
                                    minWidth: "300px", // Largeur de chaque livre correspond à la largeur visible
                                    flexShrink: 0, // Empêche les livres de rétrécir
                                }}
                            >
                                {onError ? "Erreur lors de la récupération des livres {onError}" :
                                    <BookSuggestion
                                        book={book}
                                        isFocused={index === currentIndex} // Met en avant le livre au centre
                                    />
                                }
                            </div>
                        ))}
                    </div>
                </div>

                {/* Bouton suivant */}
                <button
                    onClick={handleNext}
                    disabled={currentIndex === books.length - 1}
                    style={{
                        border: "none",
                        backgroundColor: "#4CAF50",
                        color: "#fff",
                        padding: "10px",
                        borderRadius: "5px",
                        cursor: currentIndex === books.length - 1 ? "not-allowed" : "pointer",
                        opacity: currentIndex === books.length - 1 ? 0.5 : 1,
                        transition: "opacity 0.3s",
                    }}
                >
                    →
                </button>
            </div>
        </div>
    );
};

export default Suggestions;
