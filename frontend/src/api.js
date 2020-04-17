import axios from 'axios';
import {CONFIG} from './config';
import {tokenStorage} from "./TokenStorage";

const accessToken = tokenStorage.getAccessToken();
console.log(`Access token -> ${accessToken}`);
const API_URL = CONFIG.API.URL;
let headers;
let api;

if (accessToken) {
    headers = {
        'Authorization': `Bearer ${accessToken}`
    }
}

if (headers) {
    api = axios.create({
        baseURL: API_URL,
        headers: headers
    });
} else {
    api = axios.create({
        baseURL: API_URL
    });
}
export default api