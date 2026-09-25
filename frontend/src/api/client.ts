import axios from 'axios';

const config = {
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
}

export const api = axios.create(config);


api.interceptors.request.use((config) => {
  return config;
});