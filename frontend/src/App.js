// App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import BookInfo from "./pages/BookInfo";
import ListBook from "./pages/ListBook";
import {ListBookProvider} from "./states/ListBookState";
import About from "./pages/About";
import Home from "./pages/Home";
import HeadBar from "./components/HeadBar";
import Footer from "./components/Footer";

function App() {

    return (
        <ListBookProvider>

            <Router>
                <HeadBar/>
                <Routes>
                    <Route path="/" element={<Home/>}/>
                    <Route path="/books" element={<ListBook />} />
                    <Route path="/book" element={<BookInfo />} />
                    <Route path="/about" element={<About />} />
                </Routes>
                <Footer/>
            </Router>
        </ListBookProvider>
    );
}


export default App;
