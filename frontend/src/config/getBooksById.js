import { API_BASE } from "./config";

export default function getBooksByIds(bookIDs) {
    const requestOptions = {
        method: 'GET',
        redirect: 'follow'
    };

    const bookList = [];

    const fetchPromises = bookIDs.map(bookID => {
        return fetch(`${API_BASE}/book/${encodeURIComponent(bookID)}`, requestOptions)
            .then(response => response.json())
            .then(book => {
                bookList.push(book);
            })
            .catch(error => {
                console.log(`Erreur lors de la récupération du livre avec l'ID ${bookID}:`, error);
            });
    });

    return Promise.all(fetchPromises)
        .then(() => bookList)
        .catch(error => {
            console.log('Une erreur est survenue:', error);
            return [];
        });
}
