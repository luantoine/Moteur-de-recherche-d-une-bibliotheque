import {API_BASE} from "./config";

export default function getBookById(bookID) {
    const requestOptions = {
        method: 'GET',
        redirect: 'follow'
    };

    return fetch(`${API_BASE}/book/${encodeURIComponent(bookID)}`, requestOptions)
        .then(response => {return response.json()})
        .catch(error => console.log('error', error));
}