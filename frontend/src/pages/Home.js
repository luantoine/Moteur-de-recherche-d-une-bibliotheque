import React, {useEffect, useState} from 'react';
import {useBookList} from "../states/ListBookState";
import advancedSearch from "../config/advancedSearch";
import simpleSearch from "../config/simpleSearch";

const Home = () => {

    const books = useState(null)

    const {
        listBook,
        setListBook,
        onLoading,
        setOnLoading,
        onError,
        setOnError
    } = useBookList();

    useEffect(async () => {
        try {
            setOnLoading(true);
            const searchFunction = await (searchType === "advanced" ? advancedSearch(query, LIMIT, offset) : simpleSearch(query, LIMIT, offset));
            setListBook(searchFunction);
        } catch (error) {
            setOnError("Une erreur est survenue lors de la recherche.", error.message);
        } finally {
            setOnLoading(false);
        }
    }, []);

    return (
        <div>
            
        </div>
    );
};

export default Home;