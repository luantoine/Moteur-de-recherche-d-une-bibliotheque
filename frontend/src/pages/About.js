import React from 'react';
import HeadBar from "../components/HeadBar";


const AboutUs = () => {
    return (
        <div className="min-h-screen bg-gray-100 p-8">
            <HeadBar/>w
            <div className="max-w-4xl mx-auto bg-white rounded-2xl shadow-lg p-6">
                <h1 className="text-3xl font-bold text-gray-800 mb-4">À propos de nous</h1>

                <section className="mb-6">
                    <h2 className="text-xl font-semibold text-gray-700 mb-2">Le projet : <span className="text-indigo-600">DAAR Projet Final - Choix A</span></h2>
                    <p className="text-gray-600 leading-relaxed">
                        Nous travaillons sur la création d'un moteur de recherche pour une bibliothèque numérique composée d'une vaste collection de livres textuels.
                        Ce projet vise à offrir une solution intuitive, rapide et performante pour la recherche de documents, tout en intégrant des fonctionnalités avancées telles que la recherche par mots-clés,
                        l'analyse par expressions régulières et des suggestions personnalisées.
                    </p>
                </section>

                <section className="mb-6">
                    <h2 className="text-xl font-semibold text-gray-700 mb-2">L'équipe</h2>
                    <ul className="list-disc pl-5 text-gray-600">
                        <li><strong>Nom 1</strong> : Responsable de l'architecture backend et des algorithmes de recherche. Passionné par l'optimisation des performances des moteurs de recherche.</li>
                        <li><strong>Nom 2</strong> : Chargé de l'interface utilisateur et de l'expérience client. Conçoit des interfaces élégantes et accessibles.</li>
                        <li><strong>Nom 3</strong> : Spécialiste des bases de données et de la gestion des graphes, notamment dans la mise en œuvre des graphes de Jaccard.</li>
                    </ul>
                </section>

                <section className="mb-6">
                    <h2 className="text-xl font-semibold text-gray-700 mb-2">Notre vision</h2>
                    <ul className="list-disc pl-5 text-gray-600">
                        <li><strong>Accessibilité</strong> : Fournir un accès rapide à une collection de plus de 1664 livres, chacun contenant au moins 10 000 mots.</li>
                        <li><strong>Pertinence</strong> : Mettre en œuvre des algorithmes éprouvés tels que closeness, betweenness ou pagerank pour trier et classer les résultats de recherche.</li>
                        <li><strong>Innovation</strong> : Offrir des fonctionnalités avancées comme la recherche par expressions régulières et des suggestions basées sur des graphes de Jaccard.</li>
                        <li><strong>Performance</strong> : Garantir des temps de réponse optimaux grâce à des tests rigoureux et une infrastructure performante.</li>
                    </ul>
                </section>

                <section>
                    <h2 className="text-xl font-semibold text-gray-700 mb-2">Objectifs du projet</h2>
                    <p className="text-gray-600 leading-relaxed">
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
