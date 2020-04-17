import axios from 'axios';
import {CONFIG} from './config';
import {tokenStorage} from "./TokenStorage";

const accessToken = tokenStorage.getAccessToken();
console.log(`Access token -> ${accessToken}`);
const API_URL = CONFIG.API.URL;
const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Authorization': `Bearer ${accessToken}`
    }
});
export default api