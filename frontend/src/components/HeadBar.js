import React from 'react';
import SearchBar from "./SearchBar";

const HeadBar = () => {

    return (
        <header className={"banniere"}>
            <h1 className={"titleApp"}>Databerg</h1>
            <SearchBar/>
        </header>
    );
};

export default HeadBar;
