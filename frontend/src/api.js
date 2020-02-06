import axios from 'axios';
import {CONFIG} from './config';

const API_URL = CONFIG.API.URL;

export default axios.create({
    baseURL: API_URL
})