import axios from 'axios';

// In Docker: nginx proxies /api → Flask container (no CORS, no hardcoded host).
// Locally:   set VITE_API_URL=http://localhost:5000/api in a .env file.
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      console.error('API error response:', error.response.status, error.response.data);
    } else if (error.request) {
      console.error('API no response – is the backend running?');
    } else {
      console.error('API request setup error:', error.message);
    }
    return Promise.reject(error);
  }
);

export const getGenderDistribution = (school = null, subject = null) => {
  const params = {};
  if (school)  params.school  = school;
  if (subject) params.subject = subject;
  return api.get('/gender-distribution', { params });
};

export const getAverageGrades = (school = null, subject = null) => {
  const params = {};
  if (school)  params.school  = school;
  if (subject) params.subject = subject;
  return api.get('/average-grades', { params });
};

export const getAlcoholVsPerformance = (
  consumptionLevelType = 'weekend_alcohol_consumption_level'
) => {
  return api.get('/alcohol-vs-performance', {
    params: { consumption_level_type: consumptionLevelType },
  });
};

export const healthCheck = () => api.get('/health');

export default api;
