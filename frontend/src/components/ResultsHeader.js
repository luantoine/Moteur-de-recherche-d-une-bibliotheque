import React from 'react';

const ResultsHeader = (text) => {
    return (
        <p
            style={{
                fontSize: "30px",
                fontWeight: "bold",
                textAlign: "center",
                marginBottom: "20px",
                textTransform: "uppercase",
                letterSpacing: "1px",
                fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
                background: "linear-gradient(90deg, rgba(255,99,71,1) 0%, rgba(255,165,0,1) 100%)",
                WebkitBackgroundClip: "text",
                color: "transparent",
            }}
        >
            {text.titre}
        </p>
    );
};

export default ResultsHeader;