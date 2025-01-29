import React, { useEffect, useState } from 'react';
import Loading from "../components/Loading";
import { useLocation } from "react-router-dom";
import getBookById from "../config/getBookById";
import BookDetails from "../components/BookDetails";
import Error from "../components/Error";
import Suggestions from "../components/Suggestions";

const BookInfo = () => {
    const [book, setBook] = useState(null);
    const [onLoading, setOnLoading] = useState(true);
    const [onError, setOnError] = useState(null);
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const bookId = queryParams.get("bookId");

    useEffect(() => {
        setOnLoading(true);  // Start loading before fetching
        getBookById(bookId)
            .then((book) => {
                setBook(book);
                setOnLoading(false);
                console.log(book)
            })
            .catch((error) => {
                setOnError(`Une erreur est survenue lors de la recherche: ${error}`);
                setOnLoading(false);
            })
    }, [bookId]);

    if (onLoading) return <Loading />;
    if (onError) return <Error message={onError} />;
    if (!book) {
        return <Error message={"Le livre n'existe pas!"} />;
    }

    return (
        <div className="book-details">
            <BookDetails book={book} />
            <Suggestions booksId={JSON.parse(book.neighbors).slice(0, 10)} />
        </div>
    );
};

export default BookInfo;
