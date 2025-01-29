import React from 'react';
import ResultsHeader from "../components/ResultsHeader";

const AboutUs = () => {
    return (
        <div style={{ minHeight: "100vh", background: "linear-gradient(to right, #f7f7f7, #eaeaea)", padding: "32px" }}>
            <div
                style={{
                    maxWidth: "900px",
                    margin: "0 auto",
                    background: "#fff",
                    borderRadius: "16px",
                    boxShadow: "0 10px 20px rgba(0, 0, 0, 0.1)",
                    padding: "32px",
                    transform: "scale(1)",
                    transition: "transform 0.3s",
                }}
                onMouseEnter={(e) => (e.currentTarget.style.transform = "scale(1.02)")}
                onMouseLeave={(e) => (e.currentTarget.style.transform = "scale(1)")}
            >
                <ResultsHeader titre={"À propos de nous"}/>

                <section style={{ marginBottom: "24px" }}>
                    <h2
                        style={{
                            fontSize: "24px",
                            fontWeight: "700",
                            color: "#4CAF50",
                            marginBottom: "16px",
                        }}
                    >
                        Le projet : <span style={{ color: "#4CAF50" }}>DAAR Projet Final - Choix A</span>
                    </h2>
                    <p style={{ color: "#555", lineHeight: "1.8" }}>
                        Nous travaillons sur la création d'un moteur de recherche pour une bibliothèque numérique composée d'une vaste collection de livres textuels.
                        Ce projet vise à offrir une solution intuitive, rapide et performante pour la recherche de documents, tout en intégrant des fonctionnalités avancées telles que la recherche par mots-clés,
                        l'analyse par expressions régulières et des suggestions personnalisées.
                    </p>
                </section>

                <section style={{ marginBottom: "24px" }}>
                    <h2
                        style={{
                            fontSize: "24px",
                            fontWeight: "700",
                            color: "#4CAF50",
                            marginBottom: "16px",
                        }}
                    >
                        L'équipe
                    </h2>
                    <ul style={{ paddingLeft: "20px", color: "#555", lineHeight: "1.8" }}>
                        <li><strong>Andre VICENTE</strong> : Responsable de l'architecture backend et des algorithmes de recherche. Passionné par l'optimisation des performances des moteurs de recherche.</li>
                        <li><strong>Arnaud UTHAYAKUMAR</strong> : Chargé de l'interface utilisateur et de l'expérience client. Conçoit des interfaces élégantes et accessibles.</li>
                        <li><strong>Antoine LUONG</strong> : Spécialiste des bases de données et de la gestion des graphes, notamment dans la mise en œuvre des graphes de Jaccard.</li>
                    </ul>
                </section>

                <section style={{ marginBottom: "24px" }}>
                    <h2
                        style={{
                            fontSize: "24px",
                            fontWeight: "700",
                            color: "#4CAF50",
                            marginBottom: "16px",
                        }}
                    >
                        Notre vision
                    </h2>
                    <ul style={{ paddingLeft: "20px", color: "#555", lineHeight: "1.8" }}>
                        <li><strong>Accessibilité</strong> : Fournir un accès rapide à une collection de plus de 1664 livres, chacun contenant au moins 10 000 mots.</li>
                        <li><strong>Pertinence</strong> : Mettre en œuvre des algorithmes éprouvés tels que closeness, betweenness ou pagerank pour trier et classer les résultats de recherche.</li>
                        <li><strong>Innovation</strong> : Offrir des fonctionnalités avancées comme la recherche par expressions régulières et des suggestions basées sur des graphes de Jaccard.</li>
                        <li><strong>Performance</strong> : Garantir des temps de réponse optimaux grâce à des tests rigoureux et une infrastructure performante.</li>
                    </ul>
                </section>

                <section>
                    <h2
                        style={{
                            fontSize: "24px",
                            fontWeight: "700",
                            color: "#4CAF50",
                            marginBottom: "16px",
                        }}
                    >
                        Objectifs du projet
                    </h2>
                    <p style={{ color: "#555", lineHeight: "1.8" }}>
                        Ce projet est une occasion unique de démontrer nos compétences dans la conception d'applications web et mobiles interactives,
                        l'intégration d'algorithmes avancés pour des systèmes de recherche et de recommandation,
                        et la collaboration sur un projet complet allant de la création de la bibliothèque à la démonstration finale.
                    </p>
                </section>
            </div>
        </div>
    );
};

export default AboutUs;
