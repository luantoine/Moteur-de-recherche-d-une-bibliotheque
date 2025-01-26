// Fonction pour convertir les codes de langues en noms complets
const languageMapping = {
    en: "Anglais",
    fr: "Français",
    es: "Espagnol",
    de: "Allemand",
    it: "Italien",
    zh: "Chinois",
    ja: "Japonais",
    ru: "Russe",
    ar: "Arabe",
    pt: "Portugais",
    // Ajoutez d'autres langues si nécessaire
};

export function formatLanguages (languagesArray) {
    try {
        if (!Array.isArray(languagesArray) || languagesArray.length === 0) {
            return "Non spécifié";
        }
        const formattedLanguages = languagesArray.map(
            (code) => languageMapping[code] || code // Fallback au code si inconnu
        );
        return (
            <ul style={{ paddingLeft: "20px", listStyleType: "circle", color: "#555" }}>
                {formattedLanguages.map((lang, index) => (
                    <li key={index} style={{ marginBottom: "5px" }}>
                        {lang}
                    </li>
                ))}
            </ul>
        );
    } catch (error) {
        console.error("Erreur lors du formatage des langues :", error);
        return "Non spécifié";
    }
};