import React from 'react';
import { useLocation, useNavigate } from "react-router-dom";
import { formatAuthorFromJSON } from "../format/AuthorFormat";

const BookCompact = ({ book }) => {
    const info = book;
    const navigate = useNavigate();
    const location = useLocation();

    function onBookSelect() {
        if (location.pathname !== '/book') {
            navigate(`/book?bookId=${encodeURIComponent(info.id)}`);
        }
    }

    return (
        <div
            onClick={onBookSelect}
            style={{
                display: "flex",
                alignItems: "center",
                padding: "20px",
                marginBottom: "15px",
                border: "1px solid #ddd",
                borderRadius: "10px",
                cursor: "pointer",
                boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
                backgroundColor: "#f9f9f9",
                transition: "transform 0.2s, box-shadow 0.2s",
                gap: "15px",
            }}
            onMouseOver={(e) => {
                e.currentTarget.style.transform = "scale(1.03)";
                e.currentTarget.style.boxShadow = "0 6px 12px rgba(0, 0, 0, 0.15)";
            }}
            onMouseOut={(e) => {
                e.currentTarget.style.transform = "scale(1)";
                e.currentTarget.style.boxShadow = "0 4px 8px rgba(0, 0, 0, 0.1)";
            }}
        >
            <div style={{ flexShrink: 0 }}>
                {info.cover_url && (
                    <img
                        src={info.cover_url}
                        alt={info.title}
                        style={{
                            width: "80px",
                            height: "120px",
                            borderRadius: "5px",
                            objectFit: "cover",
                        }}
                    />
                )}
            </div>

            <div style={{ flex: 1 }}>
                <h1
                    style={{
                        fontSize: "20px",
                        margin: "0 0 8px",
                        color: "#333",
                        fontWeight: "bold",
                    }}
                >
                    {info.title}
                </h1>
                <h2
                    style={{
                        fontSize: "16px",
                        margin: "0",
                        color: "#555",
                    }}
                >
                    Par {formatAuthorFromJSON(info.authors)}
                </h2>
            </div>
        </div>
    );
};

export default BookCompact;
