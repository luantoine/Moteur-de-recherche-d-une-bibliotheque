export  function formatAuthorFromJSON(jsonString) {
    if (!jsonString) {
        return "Auteur inconnu";
    }

    try {
        const authors = JSON.parse(jsonString);

        if (!Array.isArray(authors) || authors.length === 0) {
            return "Auteur inconnu";
        }

        const { name, birth_year, death_year } = authors[0];

        const years = birth_year && death_year
            ? ` (${birth_year} - ${death_year})`
            : birth_year
                ? ` (né en ${birth_year})`
                : death_year
                    ? ` (mort en ${death_year})`
                    : "";

        return `${name}${years}`;
    } catch (error) {
        console.error("Erreur lors du parsing JSON :", error);
        return "Auteur inconnu";
    }
}

