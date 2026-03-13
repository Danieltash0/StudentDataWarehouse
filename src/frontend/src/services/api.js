import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// Add response interceptor for better error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    if (error.response) {
      // Server responded with error status
      console.error('Error Response:', error.response.data);
    } else if (error.request) {
      // Request was made but no response received
      console.error('No Response:', error.request);
    } else {
      // Something else happened
      console.error('Error:', error.message);
    }
    return Promise.reject(error);
  }
);

export const getGenderDistribution = (school = null, subject = null) => {
  const params = {};
  if (school) params.school = school;
  if (subject) params.subject = subject;
  return api.get('/gender-distribution', { params });
};

export const getAverageGrades = (school = null, subject = null) => {
  const params = {};
  if (school) params.school = school;
  if (subject) params.subject = subject;
  return api.get('/average-grades', { params });
};

export const getAlcoholVsPerformance = (consumptionLevelType = 'weekend_alcohol_consumption_level') => {
  return api.get('/alcohol-vs-performance', { 
    params: { consumption_level_type: consumptionLevelType } 
  });
};

export const healthCheck = () => {
  return api.get('/health');
};

export default api;
