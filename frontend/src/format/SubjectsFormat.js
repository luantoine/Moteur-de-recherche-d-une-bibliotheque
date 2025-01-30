export function formatSubjects (subjectsString){
    try {
        const subjects = JSON.parse(subjectsString);
        if (!Array.isArray(subjects) || subjects.length === 0) {
            return "Non spécifié";
        }
        return subjects.join(", ");
    } catch (error) {
        console.error("Erreur lors du parsing des sujets :", error);
        return "Non spécifié";
    }
};