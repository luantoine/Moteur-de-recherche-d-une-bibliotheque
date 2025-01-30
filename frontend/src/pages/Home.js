import React, { useEffect, useState } from 'react';
import { useBookList } from "../states/ListBookState";
import getBestBook from "../config/getBestBook";
import Loading from "../components/Loading";
import Error from "../components/Error";
import BookList from '../components/BookList';
import ResultsHeader from "../components/ResultsHeader";
import {LIMIT_BOOK_TOSHOW, NUMBER_OF_BOOK} from "../config/config";
import Pagination from "../components/Pagination";

const Home = () => {
    const { listBook, setListBook } = useBookList();
    const [onError, setOnError] = useState(null);
    const [onLoading, setOnLoading] = useState(true);
    const [offset,setOffset] = useState(0)

    useEffect(() => {
        setOnLoading(true);  // Start loading before fetching
        getBestBook(LIMIT_BOOK_TOSHOW, offset)
            .then((bestBooks) => {
                setListBook(bestBooks);
                setOnLoading(false);
            })
            .catch((error) => {
                setOnError(`Une erreur est survenue lors de la recherche:${error}`);
                setOnLoading(false)
            })
    }, [setListBook, offset ]);

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
            <Pagination offset={offset} setOffset={setOffset} limit={LIMIT_BOOK_TOSHOW} totalResults={NUMBER_OF_BOOK} />

        </div>
    );
};

export default Home;
