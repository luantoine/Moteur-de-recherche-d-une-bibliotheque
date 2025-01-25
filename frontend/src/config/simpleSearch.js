import {API_BASE} from "./config";

export default function simpleSearch(query) {
    var requestOptions = {
        method: 'GET',
        redirect: 'follow'
    };

    return fetch(`${API_BASE}/search/?q=${encodeURIComponent(query)}`, requestOptions)
        .then(response => {return response.json()})
        .catch(error => console.log('error', error));
}