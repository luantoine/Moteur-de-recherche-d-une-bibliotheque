import React from 'react';
import HeadBar from "./HeadBar";

const Error = (message) => {

    return (
        <div >
            <HeadBar/>
           <h1>
               {message.message}
           </h1>
        </div>
    );
};

export default Error;