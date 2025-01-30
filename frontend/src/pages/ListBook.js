import React, { useEffect, useState } from "react";
import { useBookList } from "../states/ListBookState";
import Loading from "../components/Loading";
import Error from "../components/Error";
import BookList from "../components/BookList";
import { useLocation } from "react-router-dom";
import ResultsHeader from "../components/ResultsHeader";
import getBooksBySearch from "../config/getBooksBySearch";

const ListBook = () => {
    const { listBook, setListBook } = useBookList();
    const [onLoading, setOnLoading] = useState(true)
    const [onError, setOnError] = useState(null);
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const query = queryParams.get("query");
    const searchType = queryParams.get("type");
    const LIMIT = 10;
    const offset = queryParams.get("offset");

    useEffect(() => {
        if (!query) {
            setOnError("Veuillez saisir un mot-clé pour rechercher.");
            return;
        }
        try {
            setOnLoading(true);
            getBooksBySearch(query, LIMIT, offset).then((books) => {
                setListBook(books)
                setOnLoading(false)
            })
        } catch (error) {
            setOnError(`Une erreur est survenue lors de la recherche: ${error}`);
            setOnLoading(false)
        }
    }, [query, searchType, offset, setListBook]);

    if (onLoading) return <Loading />;
    if (onError) return <Error message={onError} />;
    if (!listBook || !listBook.results || listBook.results.length === 0) {
        return <Error message={"La liste de livre n'existe pas!"} />;
    }

    return (
        <div>
            <ResultsHeader titre={`Résultats des livres avec le mot <<${query}>>,${listBook.results.length} livres trouvés:`} />
            <BookList books={listBook.results} />
        </div>
    );
};

export default ListBook;
