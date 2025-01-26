import React, { useEffect, useState } from 'react';
import { useBookList } from "../states/ListBookState";
import getBestBook from "../config/getBestBook";
import HeadBar from "../components/HeadBar";
import Loading from "../components/Loading";
import Error from "../components/Error";
import BookList from '../components/BookList';

const Home = () => {
    const { listBook, setListBook, onLoading, setOnLoading } = useBookList();
    const [onError, setOnError] = useState(null);

    useEffect(() => {
        const getBestBooks = async () => {
            try {
                setOnLoading(true);
                const bestBooks = await getBestBook();
                setListBook(bestBooks);
            } catch (error) {
                setOnError("Une erreur est survenue lors de la recherche.");
            } finally {
                setOnLoading(false);
            }
        };
        getBestBooks();
    }, [setListBook, setOnError, setOnLoading]);

    if (onLoading) return <Loading />;
    if (onError) return <Error message={onError} />;
    if (!listBook || !listBook.results || listBook.results.length === 0) {
        return <Error message={"La liste de livre n'existe pas!"} />;
    }

    return (
        <div>
            <BookList books={listBook.results} />
        </div>
    );
};

export default Home;
