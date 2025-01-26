import {API_BASE} from "./config";

export default function simpleSearch(query, limit, offset) {
    var requestOptions = {
        method: 'GET',
        redirect: 'follow'
    };

    return fetch(`${API_BASE}/search/kmp/?pattern=${encodeURIComponent(query)}&limit=${encodeURIComponent(limit)}&offset=${encodeURIComponent(offset)}`, requestOptions)
        .then(response => {return response.json()})
        .catch(error => console.log('error', error));
}