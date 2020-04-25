import axios from 'axios';
import {CONFIG} from './config';
import {tokenStorage} from "./TokenStorage";

const accessToken = tokenStorage.getAccessToken();
console.log(`Access token -> ${accessToken}`);
const API_URL = CONFIG.API.URL;
let headers;

if (accessToken) {
    headers = {
        'Authorization': `Bearer ${accessToken}`
    }
}

const api = headers ? axios.create({
    baseURL: API_URL,
    headers: headers
}) : axios.create({
    baseURL: API_URL
});

export default api