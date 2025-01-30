import React, { useEffect, useState } from "react";
import { useBookList } from "../states/ListBookState";
import Loading from "../components/Loading";
import Error from "../components/Error";
import BookList from "../components/BookList";
import {useLocation, useNavigate} from "react-router-dom";
import ResultsHeader from "../components/ResultsHeader";
import getBooksBySearch from "../config/getBooksBySearch";
import {LIMIT_BOOK_TOSHOW, NUMBER_OF_BOOK} from "../config/config";
import Pagination from "../components/Pagination";

const ListBook = () => {
    const { listBook, setListBook } = useBookList();
    const [onLoading, setOnLoading] = useState(true)
    const [onError, setOnError] = useState(null);
    const location = useLocation();
    const navigate = useNavigate();
    const queryParams = new URLSearchParams(location.search);
    const query = queryParams.get("query");
    const limit = queryParams.get("limit");
    const [offset,setOffset] = useState(queryParams.get("offset"));
    console.log(offset)

    useEffect(() => {
        if (!query) {
            setOnError("Veuillez saisir un mot-clé pour rechercher.");
            return;
        }
        try {
            setOnLoading(true);
            getBooksBySearch(query, limit, offset).then((books) => {
                setListBook(books)
                setOnLoading(false)
            })
        } catch (error) {
            setOnError(`Une erreur est survenue lors de la recherche: ${error}`);
            setOnLoading(false)
        }
    }, [query, limit, offset, setListBook]);

    useEffect(() => {
        const newParams = new URLSearchParams(location.search);
        newParams.set("offset", offset);
        navigate(`${location.pathname}?${newParams.toString()}`, { replace: true });
    }, [offset, navigate, location]);

    if (onLoading) return <Loading />;
    if (onError) return <Error message={onError} />;
    if (!listBook || !listBook.results || listBook.results.length === 0) {
        return <Error message={"La liste de livre n'existe pas!"} />;
    }

    return (
        <div>
            <ResultsHeader titre={`Résultats des livres avec le mot <<${query}>>,${listBook.results.length} livres trouvés:`} />
            <BookList books={listBook.results} />
            <Pagination offset={offset} setOffset={setOffset} limit={LIMIT_BOOK_TOSHOW} totalResults={NUMBER_OF_BOOK} />
        </div>
    );
};

export default ListBook;
