import React from "react";
import { formatSubjects } from "../format/SubjectsFormat";
import { formatBookshelves } from "../format/BookShelvesFormat";
import { formatLanguages } from "../format/LanguageFormat";
import { formatAuthorFromJSON } from "../format/AuthorFormat";

const BookDetails = ({ book }) => {
    if (!book) return null; // Empêcher un crash si `book` est `undefined`

    const info = book;
    const languages = Array.isArray(info.languages) ? info.languages : JSON.parse(info.languages || "[]");

    return (
        <div
            className="book-details-container"
            style={{
                display: "flex",
                flexDirection: "row",
                alignItems: "flex-start",
                padding: "20px",
                border: "1px solid #ddd",
                borderRadius: "10px",
                marginBottom: "20px",
                boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
                maxWidth: "800px",
                margin: "auto",
                backgroundColor: "#f9f9f9",
            }}
        >
            <div style={{ marginRight: "20px" }}>
                {info.cover_url && (
                    <img
                        src={info.cover_url}
                        alt={info.title}
                        style={{
                            width: "150px",
                            height: "auto",
                            borderRadius: "8px",
                            objectFit: "cover",
                        }}
                    />
                )}
            </div>

            <div style={{ flex: 1 }}>
                <h1
                    style={{
                        fontSize: "24px",
                        margin: "0 0 10px",
                        color: "#333",
                        fontWeight: "bold",
                    }}
                >
                    {info.title}
                </h1>

                <h2
                    style={{
                        fontSize: "18px",
                        margin: "0 0 10px",
                        color: "#555",
                    }}
                >
                    Par {formatAuthorFromJSON(info.authors)}
                </h2>

                {info.subjects && (
                    <>
                        <h3 style={{ fontSize: "16px", margin: "10px 0", color: "#777" }}>Catégories :</h3>
                        {formatSubjects(info.subjects)}
                    </>
                )}

                {info.bookshelves && (
                    <>
                        <h3 style={{ fontSize: "16px", margin: "10px 0", color: "#777" }}>Étagères :</h3>
                        {formatBookshelves(info.bookshelves)}
                    </>
                )}

                {languages.length > 0 && (
                    <>
                        <h3 style={{ fontSize: "16px", margin: "10px 0", color: "#777" }}>Langues :</h3>
                        {formatLanguages(languages)}
                    </>
                )}

                <h3
                    style={{
                        fontSize: "16px",
                        margin: "10px 0",
                        color: "#777",
                    }}
                >
                    Téléchargements : {info.download_count}
                </h3>

                {info.copyright ? (
                    <p style={{ fontSize: "14px", color: "red" }}>
                        Ce livre est protégé par des droits d'auteur.
                    </p>
                ) : (
                    <>
                        <p style={{ fontSize: "14px", color: "green" }}>
                            Ce livre est dans le domaine public.
                        </p>
                        <p
                            style={{
                                fontSize: "14px",
                                color: "#333",
                                fontStyle: "italic",
                                marginTop: "20px",
                            }}
                        >
                            Vous pouvez lire <a
                            href={`https://www.gutenberg.org/cache/epub/${info.id}/pg${info.id}-images.html`}
                            target="_blank"
                            rel="noopener noreferrer"
                        >
                            ici
                        </a>.
                        </p>
                    </>
                )}
            </div>
        </div>
    );
};

export default BookDetails;
