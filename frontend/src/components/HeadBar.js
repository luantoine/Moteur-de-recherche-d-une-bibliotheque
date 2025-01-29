import React from 'react';
import { useNavigate } from 'react-router-dom';
import SearchBar from "./SearchBar";

const HeadBar = () => {
    const navigate = useNavigate();

    const handleBackClick = () => {
        navigate(-1);
    };

    const handleLogoClick = () => {
        navigate('/');
    };

    return (
        <header
            style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                padding: "20px",
                backgroundColor: "#4CAF50",
                color: "#fff",
                boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
                position: "relative",
            }}
        >
             <span
                 onClick={handleBackClick}
                 style={{
                     fontSize: "24px",
                     color: "#fff",
                     cursor: "pointer",
                     position: "absolute",
                     top: "20px",
                     left: "20px",
                     transition: "transform 0.3s ease-in-out",
                     padding: "5px 10px",
                 }}
                 onMouseOver={(e) => e.target.style.transform = "scale(1.1)"}
                 onMouseOut={(e) => e.target.style.transform = "scale(1)"} 
             >
                ←
            </span>


            <h1
                onClick={handleLogoClick}
                style={{
                    fontSize: "28px",
                    fontWeight: "bold",
                    margin: "0",
                    marginBottom: "10px",
                    cursor: "pointer"
                }}
            >
                Databerg
            </h1>

            <div style={{display: "flex", alignItems: "center"}}>


                <SearchBar/>
            </div>
        </header>
    );
};

export default HeadBar;
