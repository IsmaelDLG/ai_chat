import axios from 'axios';

const config = {
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
}

export const api = axios.create(config);


api.interceptors.request.use((config) => {
  return config;
});