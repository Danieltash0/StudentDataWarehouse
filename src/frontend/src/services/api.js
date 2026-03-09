import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

export const getGenderDistribution = (school = null, subject = null) => {
  const params = {};
  if (school) params.school = school;
  if (subject) params.subject = subject;
  return api.get('/gender-distribution', { params });
};

export const getPerformanceGrades = (school = null, subject = null) => {
  const params = {};
  if (school) params.school = school;
  if (subject) params.subject = subject;
  return api.get('/performance-grades', { params });
};

export const getAlcoholPerformance = (consumptionType = 'weekend') => {
  return api.get('/alcohol-performance', { 
    params: { consumption_type: consumptionType } 
  });
};

export const healthCheck = () => {
  return api.get('/health');
};

export default api;
