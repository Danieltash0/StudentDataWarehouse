import React, { useState, useEffect } from 'react';
import GenderPieChart from '../components/GenderPieChart';
import PerformanceBarChart from '../components/PerformanceBarChart';
import AlcoholPerformanceChart from '../components/AlcoholPerformanceChart';
import SchoolFilter from '../components/SchoolFilter';
import SubjectFilter from '../components/SubjectFilter';
import ConsumptionFilter from '../components/ConsumptionFilter';
import { 
  getGenderDistribution, 
  getAverageGrades,
  getAlcoholVsPerformance,
  healthCheck
} from '../services/api';

const Dashboard = () => {
  // Gender chart state
  const [genderData, setGenderData] = useState([]);
  const [genderLoading, setGenderLoading] = useState(true);
  const [genderSchool, setGenderSchool] = useState('');
  const [genderSubject, setGenderSubject] = useState('');

  // Performance chart state
  const [performanceData, setPerformanceData] = useState([]);
  const [performanceLoading, setPerformanceLoading] = useState(true);
  const [performanceSchool, setPerformanceSchool] = useState('');
  const [performanceSubject, setPerformanceSubject] = useState('');

  // Alcohol chart state
  const [alcoholData, setAlcoholData] = useState([]);
  const [alcoholLoading, setAlcoholLoading] = useState(true);
  const [consumptionLevelType, setConsumptionLevelType] = useState('weekend_alcohol_consumption_level');

  // Global state
  const [error, setError] = useState(null);

  // Refresh all data
  const refreshAllData = () => {
    fetchGenderData();
    fetchPerformanceData();
    fetchAlcoholData();
  };

  // Fetch gender distribution data
  useEffect(() => {
    fetchGenderData();
  }, [genderSchool, genderSubject]);

  // Fetch performance grades data
  useEffect(() => {
    fetchPerformanceData();
  }, [performanceSchool, performanceSubject]);

  // Fetch alcohol performance data
  useEffect(() => {
    fetchAlcoholData();
  }, [consumptionLevelType]);

  const fetchGenderData = async () => {
    try {
      setGenderLoading(true);
      const response = await getGenderDistribution(genderSchool, genderSubject);
      
      // Validate response data
      if (!response.data || !Array.isArray(response.data)) {
        console.warn('Invalid gender data received:', response.data);
        setGenderData([]);
      } else {
        setGenderData(response.data);
      }
      
      setError(null);
    } catch (err) {
      setError('Failed to fetch gender distribution data');
      console.error('Gender API Error:', err);
      setGenderData([]);
    } finally {
      setGenderLoading(false);
    }
  };

  const fetchPerformanceData = async () => {
    try {
      setPerformanceLoading(true);
      const response = await getAverageGrades(performanceSchool, performanceSubject);
      
      // Validate response data
      if (!response.data || !Array.isArray(response.data)) {
        console.warn('Invalid performance data received:', response.data);
        setPerformanceData([]);
      } else {
        setPerformanceData(response.data);
      }
      
      setError(null);
    } catch (err) {
      setError('Failed to fetch performance data');
      console.error('Performance API Error:', err);
      setPerformanceData([]);
    } finally {
      setPerformanceLoading(false);
    }
  };

  const fetchAlcoholData = async () => {
    try {
      setAlcoholLoading(true);
      const response = await getAlcoholVsPerformance(consumptionLevelType);
      
      // Validate response data
      if (!response.data || !Array.isArray(response.data)) {
        console.warn('Invalid alcohol data received:', response.data);
        setAlcoholData([]);
      } else {
        setAlcoholData(response.data);
      }
      
      setError(null);
    } catch (err) {
      setError('Failed to fetch alcohol performance data');
      console.error('Alcohol API Error:', err);
      setAlcoholData([]);
    } finally {
      setAlcoholLoading(false);
    }
  };

  if (error && !genderData.length && !performanceData.length && !alcoholData.length) {
    return (
      <div className="dashboard">
        <h1>Student Analytics Dashboard</h1>
        <div className="error">{error}</div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Student Analytics Dashboard</h1>
        <button onClick={refreshAllData} className="refresh-button">
          Refresh Data
        </button>
      </div>
      
      {/* Gender Distribution Section */}
      <div className="chart-section">
        <h2>Gender Distribution</h2>
        <div className="filters-row">
          <SchoolFilter school={genderSchool} setSchool={setGenderSchool} />
          <SubjectFilter subject={genderSubject} setSubject={setGenderSubject} />
        </div>
        <GenderPieChart data={genderData} loading={genderLoading} />
      </div>
      
      {/* Average Student Grades Section */}
      <div className="chart-section">
        <h2>Average Student Grades</h2>
        <div className="filters-row">
          <SchoolFilter school={performanceSchool} setSchool={setPerformanceSchool} />
          <SubjectFilter subject={performanceSubject} setSubject={setPerformanceSubject} />
        </div>
        <PerformanceBarChart data={performanceData} loading={performanceLoading} />
      </div>
      
      {/* Alcohol Consumption vs Performance Section */}
      <div className="chart-section">
        <h2>Alcohol Consumption vs Academic Performance</h2>
        <div className="filters-row">
          <ConsumptionFilter 
            consumptionType={consumptionLevelType} 
            setConsumptionType={setConsumptionLevelType} 
          />
        </div>
        <AlcoholPerformanceChart data={alcoholData} loading={alcoholLoading} />
      </div>
    </div>
  );
};

export default Dashboard;
