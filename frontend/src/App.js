import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import BookInfo from "./pages/BookInfo";
import ListBook from "./pages/ListBook";
import { ListBookProvider } from "./states/ListBookState";
import About from "./pages/About";
import Home from "./pages/Home";
import HeadBar from "./components/HeadBar";
import Footer from "./components/Footer";
import Sidebar from "./components/SideBar";

function App() {

    return (
        <ListBookProvider>
            <Router>
                <HeadBar />

                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/books" element={<ListBook />} />
                        <Route path="/book" element={<BookInfo />} />
                        <Route path="/about" element={<About />} />
                        <Route path="/*" element={<Navigate to="/" />} />
                    </Routes>

                <Footer />
            </Router>
        </ListBookProvider>
    );
}

export default App;
