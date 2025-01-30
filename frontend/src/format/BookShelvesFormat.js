export function formatBookshelves (bookshelvesString) {
    try {
        const bookshelves = JSON.parse(bookshelvesString);
        if (!Array.isArray(bookshelves) || bookshelves.length === 0) {
            return "Non spécifié";
        }
        return bookshelves.join(", ");
    } catch (error) {
        console.error("Erreur lors du parsing des étagères :", error);
        return "Non spécifié";
    }
};