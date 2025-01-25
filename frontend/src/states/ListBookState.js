import { createContext, useContext, useState } from 'react';
import getBestBook from "../config/getBestBook";
const ListBookContext = createContext();

export const ListBookProvider = ({ children }) => {
    const [listBook, setListBook] = useState(getBestBook());
    const [onLoading, setOnLoading] = useState(false);
    const [onError, setOnError ] = useState(null)

    return (
        <ListBookContext.Provider value={{ listBook, setListBook, onLoading, setOnLoading, onError, setOnError  }}>
            {children}
        </ListBookContext.Provider>
    );
};

export const useBookList = () => useContext(ListBookContext);