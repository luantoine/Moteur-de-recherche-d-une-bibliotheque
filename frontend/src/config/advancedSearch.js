import {API_BASE} from "./config";

export default function advancedSearch(query) {
    var requestOptions = {
        method: 'GET',
        redirect: 'follow'
    };

    return fetch(`${API_BASE}/advanced_search/?regex=${encodeURIComponent(query)}`, requestOptions)
        .then(response => {return response.json()})
        .catch(error => console.log('error', error));
}