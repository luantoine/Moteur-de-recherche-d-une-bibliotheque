import React from "react";

const Pagination = ({ offset, setOffset, limit, totalResults}) => {


    const handleNext = () => {
        if (offset + limit < totalResults) {
            setOffset(offset + limit);
        }
    };

    const handlePrevious = () => {
        if (offset - limit >= 0) {
            setOffset(offset - limit);
        }
    };

    return (
        <div style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            marginTop: "20px",
            gap: "10px"
        }}>
            <button
                onClick={handlePrevious}
                disabled={offset === 0}
                style={{
                    padding: "10px 15px",
                    borderRadius: "5px",
                    border: "1px solid #ccc",
                    backgroundColor: offset === 0 ? "#ddd" : "#4CAF50",
                    color: "#fff",
                    cursor: offset === 0 ? "not-allowed" : "pointer"
                }}
            >
                Précédent
            </button>
            <span style={{ fontSize: "16px", fontWeight: "bold" }}>
                Page {Math.floor(offset / limit) + 1}
            </span>
            <button
                onClick={handleNext}
                disabled={offset + limit >= totalResults}
                style={{
                    padding: "10px 15px",
                    borderRadius: "5px",
                    border: "1px solid #ccc",
                    backgroundColor: offset + limit >= totalResults ? "#ddd" : "#4CAF50",
                    color: "#fff",
                    cursor: offset + limit >= totalResults ? "not-allowed" : "pointer"
                }}
            >
                Suivant
            </button>
        </div>
    );
};

export default Pagination;
