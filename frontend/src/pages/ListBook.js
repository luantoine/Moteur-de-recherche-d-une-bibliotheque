import React, {Suspense, useEffect} from "react";
import HeadBar from "../components/HeadBar";
import { useBookList } from "../states/ListBookState";
import Book from "../components/Book";
import Loading from "../components/Loading";
import Error from "../components/Error";
import { useLocation } from "react-router-dom";
import { ADVANCED_SEARCH_API, SIMPLE_SEARCH_API } from "../config/api";

const ListBook = () => {
    const { listBook, setListBook, onLoading, setOnLoading, onError, setOnError } = useBookList();
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const query = queryParams.get("query");
    const searchType = queryParams.get("type");

    useEffect(() => {
        const searchWord = async () => {
            if (!query) {
                setOnError("Veuillez saisir un mot-clé pour rechercher.");
                return;
            }
            setOnLoading(true);
            setOnError(null);

            try {
                const uri = searchType === "advanced" ? ADVANCED_SEARCH_API : SIMPLE_SEARCH_API;
                const response = await fetch(`${uri}?query=${encodeURIComponent(query)}`);
                const data = await response.json();
<Suspense></Suspense>
                if (!response.ok) {
                    throw new Error(data.message || "Erreur lors de la recherche.");
                }

                setListBook(data);
            } catch (error) {
                setOnError(`Une erreur a été constatée : ${error.message}`);
            } finally {
                setOnLoading(false);
            }
        };

        searchWord();
    }, [query, searchType, setListBook, setOnLoading, setOnError]);

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
                <Error message={onError} />
            </div>
        );
    }

    if (!listBook || !listBook.results || listBook.results.length === 0) {
        return (
            <div>
                <HeadBar />
                <p>Aucun livre trouvé.</p>
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
