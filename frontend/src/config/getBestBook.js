import {API_BASE} from "./config";

export default function getBestBook() {
    const requestOptions = {
        method: 'GET',
        redirect: 'follow'
    };

    return fetch(`${API_BASE}/get-books-centrality/`, requestOptions)
        .then(response => {return response.json()})
        .catch(error => console.log('error', error));
}