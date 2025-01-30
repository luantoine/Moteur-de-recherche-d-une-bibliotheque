import React from 'react';
import BookCompact from "./BookCompact";

const BookList = ({ books }) => {
    return (
        <ul style={{
            display: 'flex',
            flexWrap: 'wrap',
            justifyContent: 'space-between',
            listStyleType: 'none',
            padding: '0',
            margin: '20px auto',
            maxWidth: '1200px',
        }}>
            {books.map((book) => (
                <li key={book.id} style={{
                    flexBasis: 'calc(33.33% - 20px)',
                    marginBottom: '20px',
                    boxSizing: 'border-box',
                }}>
                    <BookCompact book={book} />
                </li>
            ))}
        </ul>
    );
};

export default BookList;
