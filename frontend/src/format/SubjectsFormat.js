import React from "react";

export function formatSubjects (subjectsString) {
    try {
        const subjects = JSON.parse(subjectsString);
        if (!Array.isArray(subjects) || subjects.length === 0) {
            return "Non spécifié";
        }

        return (
            <ul style={{ paddingLeft: "20px", listStyleType: "circle", color: "#555" }}>
                {subjects.map((subject, index) => (
                    <li key={index} style={{ marginBottom: "5px" }}>
                        {subject}
                    </li>
                ))}
            </ul>
        );
    } catch (error) {
        console.error("Erreur lors du parsing des sujets :", error);
        return "Non spécifié";
    }
};