// src/lib/apiClient.ts
import axios from 'axios';

// Create a single, configured axios instance
const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api/v1', // Your FastAPI backend URL
  timeout: 10000, // 10 second timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;