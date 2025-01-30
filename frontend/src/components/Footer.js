import React from "react";

const Footer = () => {
    return (
        <footer
            style={{
                backgroundColor: "#4CAF50",
                color: "#fff",
                padding: "20px 40px",
                marginTop: "40px",
                boxShadow: "0 -4px 8px rgba(0, 0, 0, 0.1)",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
            }}
        >
            <div style={{ display: "flex", justifyContent: "space-between", width: "100%", maxWidth: "1200px" }}>
                {/* Section gauche */}
                <div>
                    <h3 style={{ fontSize: "18px", marginBottom: "10px" }}>À propos de nous</h3>
                    <p style={{ fontSize: "14px", lineHeight: "1.6", maxWidth: "300px" }}>
                        Databerg est une initiative visant à offrir une bibliothèque numérique intuitive et performante, accessible à tous.
                    </p>
                </div>

                {/* Liens utiles */}
                <div>
                    <h3 style={{ fontSize: "18px", marginBottom: "10px" }}>Liens utiles</h3>
                    <ul style={{ listStyleType: "none", padding: "0" }}>
                        <li>
                            <a
                                href="/"
                                style={{
                                    textDecoration: "none",
                                    color: "#fff",
                                    fontSize: "14px",
                                    transition: "color 0.3s",
                                }}
                                onMouseEnter={(e) => (e.target.style.color = "#c3e88d")}
                                onMouseLeave={(e) => (e.target.style.color = "#fff")}
                            >
                                Accueil
                            </a>
                        </li>
                        <li>
                            <a
                                href="/about"
                                style={{
                                    textDecoration: "none",
                                    color: "#fff",
                                    fontSize: "14px",
                                    transition: "color 0.3s",
                                }}
                                onMouseEnter={(e) => (e.target.style.color = "#c3e88d")}
                                onMouseLeave={(e) => (e.target.style.color = "#fff")}
                            >
                                À propos
                            </a>
                        </li>
                        <li>
                            <a
                                href="/books"
                                style={{
                                    textDecoration: "none",
                                    color: "#fff",
                                    fontSize: "14px",
                                    transition: "color 0.3s",
                                }}
                                onMouseEnter={(e) => (e.target.style.color = "#c3e88d")}
                                onMouseLeave={(e) => (e.target.style.color = "#fff")}
                            >
                                Explorer les livres
                            </a>
                        </li>
                    </ul>
                </div>

            </div>

            <div
                style={{
                    borderTop: "1px solid rgba(255, 255, 255, 0.2)",
                    marginTop: "20px",
                    paddingTop: "10px",
                    fontSize: "12px",
                    textAlign: "center",
                }}
            >
                &copy; {new Date().getFullYear()} Databerg. Tous droits réservés.
            </div>
        </footer>
    );
};

export default Footer;
