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

            <div style={{ display: "flex", alignItems: "center", marginBottom: "10px" }}>
                <img
                    src="frog.png" // Replace with your logo's file path
                    alt="Databerg Logo"
                    onClick={handleLogoClick}
                    style={{
                        width: "50px", // Adjust the width of the logo
                        height: "auto",
                        cursor: "pointer",
                        marginRight: "10px", // Space between the logo and the site name
                    }}
                />
                <h1
                    onClick={handleLogoClick}
                    style={{
                        fontSize: "28px",
                        fontWeight: "bold",
                        margin: "0",
                        cursor: "pointer",
                    }}
                >
                    Databerg
                </h1>
            </div>

            <div style={{ display: "flex", alignItems: "center" }}>
                <SearchBar />
            </div>
        </header>
    );
};

export default HeadBar;
