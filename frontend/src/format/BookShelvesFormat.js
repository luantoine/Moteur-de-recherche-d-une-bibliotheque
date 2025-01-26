export function formatBookshelves(bookshelvesString) {
    try {
        const bookshelves = JSON.parse(bookshelvesString);
        if (!Array.isArray(bookshelves) || bookshelves.length === 0) {
            return "Non spécifié";
        }

        return (
            <ul style={{ paddingLeft: "20px", listStyleType: "disc", color: "#555" }}>
                {bookshelves.map((shelf, index) => (
                    <li key={index} style={{ marginBottom: "5px" }}>
                        {shelf}
                    </li>
                ))}
            </ul>
        );
    } catch (error) {
        console.error("Erreur lors du parsing des étagères :", error);
        return "Non spécifié";
    }
}