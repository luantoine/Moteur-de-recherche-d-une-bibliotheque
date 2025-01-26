import React, {useEffect, useState} from 'react';
import HeadBar from "../components/HeadBar";
import Loading from "../components/Loading";
import {useLocation} from "react-router-dom";
import getBookById from "../config/getBookById";
import BookDetails from "../components/BookDetails";

const BookInfo = () => {

    const [book,setBook] = useState(null)
    const [loading,setLoading] = useState(true);
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const bookId = queryParams.get("bookId");

    useEffect(() => {

        const getBookInfo = async () => {
            setLoading(true)
            const response = await getBookById(bookId)
            setBook(response)
            setLoading(false)
        }
        getBookInfo()
    }, [bookId]);

    if(loading){
        return (
            <div>
                <Loading/>
            </div>
        )
    }

    return (
        <div className="book-details">
            <BookDetails book={book}/>
        </div>
    );
};

export default BookInfo;