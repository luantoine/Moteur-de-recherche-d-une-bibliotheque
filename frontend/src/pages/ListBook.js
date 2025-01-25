import React, { useEffect } from 'react';
import HeadBar from "../components/HeadBar";
import { useBookList } from "../states/ListBookState";
import Book from "../components/Book";
import Loading from "../components/Loading";
import Error from "../components/Error";
import { useLocation } from "react-router-dom";
import {ADVANCED_SEARCH_API, SIMPLE_SEARCH_API} from "../config/api";

const ListBook = () => {
    const { listBook, onLoading, onError, setListBook, setOnLoading, setOnError } = useBookList()
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const query = queryParams.get("query");
    const searchType = queryParams.get("type")

    useEffect(() => {
        const searchWord = async () => {
            if (!query) return; // Pas de recherche sans mot-clé
            setOnLoading(true);
            try {
                let uri = "";
                searchType === "advanced" ?
                    uri = ADVANCED_SEARCH_API:
                    uri = SIMPLE_SEARCH_API
                const response = await fetch(uri)
                const data = await response.json();
                setOnLoading(false);
                if (!response.ok) {
                    setOnError(data.message || "Erreur lors de la recherche.");
                } else {
                    setListBook(data);
                    setOnError(null);
                }
            } catch (error) {
                setOnLoading(false);
                setOnError(`Une erreur a été constatée : ${error.message || "Erreur inconnue"}`);
            }
        };
        searchWord();
    }, [query, searchType]);

    if (!query) {
        setOnLoading(false)
        setOnError("Veuillez saisir un mot-clé pour rechercher." )
    }

    if (!listBook || !listBook.results || listBook.results.length === 0) {
        setOnLoading(false)
        setOnError("Aucun livre trouvé")
    }

    if (onLoading) {
        return (
            <div>
                <HeadBar />
                <Loading />
            </div>
        );
    }

    if (onError) {
        return (
            <div>
                <HeadBar />
                <Error />
            </div>
        );
    }

    return (
        <div>
            <HeadBar />
            <ul className="book-list">
                {listBook.results.map((book) => (
                    <li key={book.id} className="book-item">
                        <Book book={book} withInfo={false} />
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default ListBook;
