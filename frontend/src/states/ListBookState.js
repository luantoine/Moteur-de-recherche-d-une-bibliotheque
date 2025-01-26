import { createContext, useContext, useState } from 'react';
import getBestBook from "../config/getBestBook";
const ListBookContext = createContext();

export const ListBookProvider = ({ children }) => {
    const [listBook, setListBook] = useState(getBestBook());
    const [onLoading, setOnLoading] = useState(false);

    return (
        <ListBookContext.Provider value={{ listBook, setListBook, onLoading, setOnLoading}}>
            {children}
        </ListBookContext.Provider>
    );
};

export const useBookList = () => useContext(ListBookContext);