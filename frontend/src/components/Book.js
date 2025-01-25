import React from 'react';

const Book = (book, withInfo) => {

    const info = book.book
    
    function formatAuthorFromJSON(jsonString) {
        if (!jsonString) {
            return "Auteur inconnu";
        }

        try {
            const authors = JSON.parse(jsonString);

            if (!Array.isArray(authors) || authors.length === 0) {
                return "Auteur inconnu";
            }

            const { name, birth_year, death_year } = authors[0];

            const years = birth_year && death_year
                ? ` (${birth_year} - ${death_year})`
                : birth_year
                    ? ` (né en ${birth_year})`
                    : death_year
                        ? ` (mort en ${death_year})`
                        : "";

            return `${name}${years}`;
        } catch (error) {
            console.error("Erreur lors du parsing JSON :", error);
            return "Auteur inconnu";
        }
    }


    function onBookSelect(book) {
        console.log("Livre sélectionné :", book);
    }

    return (
        <div
            onClick={() => onBookSelect(book)}
            style={{
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                marginBottom: '10px'
            }}>
            <div>
                {info.cover_url && (
                    <img
                        src={info.cover_url}
                        alt={info.title}
                        className="book-cover"
                        style={{width: '50px', marginRight: '10px'}}
                    />
                )}
            </div>

            <div>
                <h1>
                    <strong>{info.title}</strong>
                </h1>
                <h3>
                par {formatAuthorFromJSON(info.authors)}
                </h3>
            </div>
        </div>
    );
};

export default Book;