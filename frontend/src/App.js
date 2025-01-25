// App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import BookInfo from "./pages/BookInfo";
import ListBook from "./pages/ListBook";
import {ListBookProvider} from "./states/ListBookState";
import About from "./pages/About";

function App() {

    return (
        <ListBookProvider>
            <Router>
                <Routes>
                    <Route path="/" element={<ListBook/>}/>
                    <Route path="/books" element={<ListBook />} />
                    <Route path="/book" element={<BookInfo />} />
                    <Route path="/about" element={<About />} />
                </Routes>
            </Router>
        </ListBookProvider>
    );
}


export default App;
