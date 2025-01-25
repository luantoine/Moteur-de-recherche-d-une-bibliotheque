import React from 'react';
import {useBookList} from "../states/ListBookState";

const Error = () => {

    const { onError } = useBookList();

    return (
        <div className={"container"}>
           <h1>
               {onError}
           </h1>
        </div>
    );
};

export default Error;