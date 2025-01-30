import {API_BASE} from "./config";

export default function getBestBook(limit, offset) {
    const requestOptions = {
        method: 'GET',
        redirect: 'follow'
    };

    return fetch(`${API_BASE}/get-books-centrality?limit=${limit}&offset=${offset}`, requestOptions)
        .then(response => {return response.json()})
        .catch(error => console.log('error', error));
}