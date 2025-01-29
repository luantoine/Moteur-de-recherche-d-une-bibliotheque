import React from "react";
import { useNavigate } from "react-router-dom";

const Sidebar = () => {
    const navigate = useNavigate();

    return (
        <div
            style={{
                height: "100vh",
                width: "250px",
                backgroundColor: "#4CAF50",
                color: "#fff",
                position: "fixed",
                top: 0,
                left: 0,
                display: "flex",
                flexDirection: "column",
                padding: "20px",
                boxShadow: "2px 0 8px rgba(0, 0, 0, 0.1)",
            }}
        >
            <h2 style={{ fontSize: "20px", marginBottom: "20px", textAlign: "center" }}>
                Navigation
            </h2>

            <ul style={{ listStyleType: "none", padding: 0, margin: 0 }}>
                {[
                    { label: "Accueil", path: "/" },
                    { label: "Explorer les livres", path: "/books" },
                    { label: "À propos", path: "/about" },
                ].map((link, index) => (
                    <li
                        key={index}
                        style={{
                            marginBottom: "15px",
                        }}
                    >
                        <button
                            onClick={() => navigate(link.path)}
                            style={{
                                background: "none",
                                border: "none",
                                color: "#fff",
                                fontSize: "16px",
                                textAlign: "left",
                                width: "100%",
                                padding: "10px",
                                borderRadius: "5px",
                                transition: "background 0.3s",
                                cursor: "pointer",
                            }}
                            onMouseEnter={(e) => (e.target.style.background = "#3E8E41")}
                            onMouseLeave={(e) => (e.target.style.background = "none")}
                        >
                            {link.label}
                        </button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Sidebar;
