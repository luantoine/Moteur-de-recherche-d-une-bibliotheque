import React from 'react';
import { useNavigate } from "react-router-dom";
import { formatAuthorFromJSON } from "../format/AuthorFormat";

const BookSuggestion = ({ book }) => {
    const navigate = useNavigate();

    const onBookSelect = () => {
        navigate(`/book?bookId=${encodeURIComponent(book.id)}`);
    };

    return (
        <div
            onClick={onBookSelect}
            style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                padding: "15px",
                margin: "10px",
                border: "2px solid #ddd",
                borderRadius: "12px",
                cursor: "pointer",
                boxShadow: "0 6px 12px rgba(0, 0, 0, 0.15)",
                backgroundColor: "#fff",
                transition: "transform 0.2s, box-shadow 0.2s",
                width: "200px",
                textAlign: "center",
            }}
            onMouseOver={(e) => {
                e.currentTarget.style.transform = "scale(1.05)";
                e.currentTarget.style.boxShadow = "0 8px 16px rgba(0, 0, 0, 0.2)";
            }}
            onMouseOut={(e) => {
                e.currentTarget.style.transform = "scale(1)";
                e.currentTarget.style.boxShadow = "0 6px 12px rgba(0, 0, 0, 0.15)";
            }}
        >
            {book.cover_url && (
                <img
                    src={book.cover_url}
                    alt={book.title}
                    style={{
                        width: "120px",
                        height: "180px",
                        objectFit: "cover",
                        marginBottom: "10px",
                    }}
                />
            )}
            <h1
                style={{
                    fontSize: "16px",
                    margin: "0 0 8px",
                    color: "#333",
                    fontWeight: "bold",
                }}
            >
                {book.title}
            </h1>
            <h2
                style={{
                    fontSize: "14px",
                    margin: "0",
                    color: "#555",
                }}
            >
                Par {formatAuthorFromJSON(book.authors)}
            </h2>
        </div>
    );
};

export default BookSuggestion;
