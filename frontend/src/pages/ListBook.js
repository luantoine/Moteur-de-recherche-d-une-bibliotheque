import React, {useEffect, useState} from "react";
import HeadBar from "../components/HeadBar";
import { useBookList } from "../states/ListBookState";
import Book from "../components/Book";
import Loading from "../components/Loading";
import Error from "../components/Error";
import { useLocation } from "react-router-dom";
import advancedSearch from "../config/advancedSearch";
import simpleSearch from "../config/simpleSearch";

const ListBook = () => {
    const {
        listBook,
        setListBook,
        onLoading,
        setOnLoading
    } = useBookList();

    const {onError, setOnError} = useState(null)
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
                const searchFunction = await (searchType === "advanced" ? advancedSearch(query, LIMIT, offset) : simpleSearch(query, LIMIT, offset));
                setListBook(searchFunction);
            } catch (error) {
                setOnError("Une erreur est survenue lors de la recherche.", error.message);
            } finally {
                setOnLoading(false);
            }
        };
        searchWord();
    }, [query, searchType]);

    if (onLoading) {
        return (
            <Loading />
        );
    }

    if (onError) {
        return (
            <Error message={onError} />
        );
    }

    if (!listBook || !listBook.results || listBook.results.length === 0) {
        return (
            <Error message={"La liste de livre n'existe pas!"} />
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
