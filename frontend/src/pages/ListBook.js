import React, { useEffect, useState } from "react";
import { useBookList } from "../states/ListBookState";
import advancedSearch from "../config/advancedSearch";
import simpleSearch from "../config/simpleSearch";
import Loading from "../components/Loading";
import Error from "../components/Error";
import BookList from "../components/BookList";
import { useLocation } from "react-router-dom";

const ListBook = () => {
    const { listBook, setListBook, onLoading, setOnLoading } = useBookList();
    const [onError, setOnError] = useState(null);
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const query = queryParams.get("query");
    const searchType = queryParams.get("type");
    const LIMIT = 10;
    const offset = queryParams.get("offset");

    useEffect(() => {
        const searchWord = async () => {
            if (!query) {
                setOnError("Veuillez saisir un mot-clé pour rechercher.");
                return;
            }
            try {
                setOnLoading(true);
                const searchFunction = searchType === "advanced"
                    ? await advancedSearch(query, LIMIT, offset)
                    : await simpleSearch(query, LIMIT, offset);
                setListBook(searchFunction);
            } catch (error) {
                setOnError("Une erreur est survenue lors de la recherche.");
            } finally {
                setOnLoading(false);
            }
        };
        searchWord();
    }, [query, searchType, setListBook, setOnError, setOnLoading, offset]);

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

export default ListBook;
