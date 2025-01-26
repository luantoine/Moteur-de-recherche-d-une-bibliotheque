import React, {useEffect, useState} from 'react';
import {useBookList} from "../states/ListBookState";
import getBestBook from "../config/getBestBook";
import HeadBar from "../components/HeadBar";
import Book from "../components/Book";
import Loading from "../components/Loading";
import Error from "../components/Error";

const Home = () => {

    const {
        listBook,
        setListBook,
        onLoading,
        setOnLoading
    } = useBookList();

    const {onError, setOnError} = useState(null)

    useEffect(()=>{
        const getBestBooks = async () => {
            try {
                setOnLoading(true);
                const bestBooks = await getBestBook();
                console.log("la",bestBooks)
                setListBook(bestBooks);
            } catch (error) {
                setOnError("Une erreur est survenue lors de la recherche.", error.message);
            } finally {
                setOnLoading(false);
            }
        }
        getBestBooks();
    }, []);

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

export default Home;