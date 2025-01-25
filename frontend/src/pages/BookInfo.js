import React from 'react';
import Book from "../components/Book";

const BookInfo = (book) => {
    return (
        <div>
            <Book book={book} withInfo={true}/>
        </div>
    );
};

export default BookInfo;