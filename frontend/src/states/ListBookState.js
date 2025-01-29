import { createContext, useContext, useState } from 'react';
import getBestBook from "../config/getBestBook";
const ListBookContext = createContext();

export const ListBookProvider = ({ children }) => {
    const [listBook, setListBook] = useState(getBestBook());

    return (
        <ListBookContext.Provider value={{ listBook, setListBook}}>
            {children}
        </ListBookContext.Provider>
    );
};

export const useBookList = () => useContext(ListBookContext);