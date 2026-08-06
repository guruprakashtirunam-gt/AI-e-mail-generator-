import axios from 'axios';

const API_URL = 'http://localhost:8000'; // Change to production URL when deployed

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  processVideo: async (url) => {
    const response = await apiClient.post('/process-video', { youtube_url: url });
    return response.data;
  },
  chat: async (question) => {
    const response = await apiClient.post('/chat', { question });
    return response.data;
  }
};
