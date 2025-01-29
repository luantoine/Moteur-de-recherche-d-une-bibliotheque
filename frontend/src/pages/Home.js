import React, { useEffect, useState } from 'react';
import { useBookList } from "../states/ListBookState";
import getBestBook from "../config/getBestBook";
import Loading from "../components/Loading";
import Error from "../components/Error";
import BookList from '../components/BookList';
import ResultsHeader from "../components/ResultsHeader";

const Home = () => {
    const { listBook, setListBook } = useBookList();
    const [onError, setOnError] = useState(null);
    const [onLoading, setOnLoading] = useState(true);

    useEffect(() => {
        setOnLoading(true);  // Start loading before fetching
        getBestBook()
            .then((bestBooks) => {
                setListBook(bestBooks);
                setOnLoading(false);
            })
            .catch((error) => {
                setOnError(`Une erreur est survenue lors de la recherche:${error}`);
                setOnLoading(false)
            })
    }, [setListBook]);

    if (onLoading) return <Loading />;
    if (onError) return <Error message={onError} />;
    if (!listBook || !listBook.results || listBook.results.length === 0) {
        return <Error message={"La liste de livre n'existe pas!"} />;
    }

    return (
        <div>
            <ResultsHeader titre={"BIENVENUE DANS DATABERG"} />
            <ResultsHeader titre={"Résultats des meilleurs livres selon notre algorithme"} />
            <BookList books={listBook.results} />
        </div>
    );
};

export default Home;
