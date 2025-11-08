import axios from 'axios';

const API_URL = 'http://localhost:8000';

// Create axios instance with base URL
const api = axios.create({
  baseURL: API_URL,
  withCredentials: true, // Enable sending cookies with requests
  headers: {
    'Access-Control-Allow-Origin': '*'
  }
});

export const auth = {
  login: async (username, password) => {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    
    const response = await api.post('/users/token', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
    return response.data;
  },

  signup: async (userData) => {
    const response = await api.post('/users/signin', userData);
    return response.data;
  },

  getCurrentUser: async () => {
    const response = await api.get('/users/me/');
    return response.data;
  },

  logout: async () => {
    const response = await api.post('/users/logout/');
    return response.data;
  }
};

export const leaderboard = {
  getLeaderboard: async () => {
    const response = await api.get('/leaderboard/');
    return response.data;
  },

  updateUserScore: async (score_change) => {
    const response = await api.patch('/users/score/update', { "score_change": score_change });
    return response.data;
  }
};

export const verses = {
    getRandomVerse: async () => {
    const response = await api.get('/verses/random');
    return response.data;
  },
  
    getAllVerses: async () => {
    const response = await api.get('/verses/');
    return response.data;
  },

  getVersesByBook: async (book) => {
    const response = await api.get(`/verses/${book}`);
    return response.data;
  },

  getVersesByChapter: async (book, chapter) => {
    const response = await api.get(`/verses/${book}/${chapter}`);
    return response.data;
  },

  getVerseByReference: async (book, chapter, verse) => {
    const response = await api.get(`/verses/${book}/${chapter}/${verse}`);
    return response.data;
  }
};

export default {
  auth,
  verses,
};