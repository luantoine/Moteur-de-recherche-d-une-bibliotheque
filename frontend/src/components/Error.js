import React from 'react';

const Error = (message) => {

    return (
        <div className={"container"}>
           <h1>
               {message.message}
           </h1>
        </div>
    );
};

export default Error;