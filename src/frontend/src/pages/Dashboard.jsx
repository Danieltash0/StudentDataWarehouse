import React, { useState, useEffect, useCallback } from 'react';
import GenderPieChart         from '../components/GenderPieChart';
import PerformanceBarChart    from '../components/PerformanceBarChart';
import AlcoholPerformanceChart from '../components/AlcoholPerformanceChart';
import SchoolFilter           from '../components/SchoolFilter';
import SubjectFilter          from '../components/SubjectFilter';
import ConsumptionFilter      from '../components/ConsumptionFilter';
import {
  getGenderDistribution,
  getAverageGrades,
  getAlcoholVsPerformance,
} from '../services/api';

// ── Reusable chart section wrapper ────────────────────────────────────────────
const ChartSection = ({ title, filters, children, error }) => (
  <section className="chart-section">
    <div className="section-header">
      <h2>{title}</h2>
    </div>
    {filters && <div className="filters-row">{filters}</div>}
    {error && <div className="inline-error">{error}</div>}
    {children}
  </section>
);

// ── Dashboard ─────────────────────────────────────────────────────────────────
const Dashboard = () => {

  // Gender chart
  const [genderData,    setGenderData]    = useState([]);
  const [genderLoading, setGenderLoading] = useState(true);
  const [genderError,   setGenderError]   = useState(null);
  const [genderSchool,  setGenderSchool]  = useState('');
  const [genderSubject, setGenderSubject] = useState('');

  // Performance chart
  const [perfData,    setPerfData]    = useState([]);
  const [perfLoading, setPerfLoading] = useState(true);
  const [perfError,   setPerfError]   = useState(null);
  const [perfSchool,  setPerfSchool]  = useState('');
  const [perfSubject, setPerfSubject] = useState('');

  // Alcohol chart
  const [alcoholData,    setAlcoholData]    = useState([]);
  const [alcoholLoading, setAlcoholLoading] = useState(true);
  const [alcoholError,   setAlcoholError]   = useState(null);
  const [consumptionType, setConsumptionType] = useState('weekend_alcohol_consumption_level');

  // ── Fetchers ────────────────────────────────────────────────────────────────
  const fetchGender = useCallback(async () => {
    setGenderLoading(true);
    setGenderError(null);
    try {
      const { data } = await getGenderDistribution(genderSchool, genderSubject);
      setGenderData(Array.isArray(data) ? data : []);
    } catch {
      setGenderError('Could not load gender data. Is the API running?');
      setGenderData([]);
    } finally {
      setGenderLoading(false);
    }
  }, [genderSchool, genderSubject]);

  const fetchPerf = useCallback(async () => {
    setPerfLoading(true);
    setPerfError(null);
    try {
      const { data } = await getAverageGrades(perfSchool, perfSubject);
      setPerfData(Array.isArray(data) ? data : []);
    } catch {
      setPerfError('Could not load grade data. Is the API running?');
      setPerfData([]);
    } finally {
      setPerfLoading(false);
    }
  }, [perfSchool, perfSubject]);

  const fetchAlcohol = useCallback(async () => {
    setAlcoholLoading(true);
    setAlcoholError(null);
    try {
      const { data } = await getAlcoholVsPerformance(consumptionType);
      setAlcoholData(Array.isArray(data) ? data : []);
    } catch {
      setAlcoholError('Could not load alcohol data. Is the API running?');
      setAlcoholData([]);
    } finally {
      setAlcoholLoading(false);
    }
  }, [consumptionType]);

  // ── Effects ─────────────────────────────────────────────────────────────────
  useEffect(() => { fetchGender();  }, [fetchGender]);
  useEffect(() => { fetchPerf();    }, [fetchPerf]);
  useEffect(() => { fetchAlcohol(); }, [fetchAlcohol]);

  const refreshAll = () => { fetchGender(); fetchPerf(); fetchAlcohol(); };

  // ── Render ───────────────────────────────────────────────────────────────────
  return (
    <div className="dashboard">

      {/* ── Header ── */}
      <header className="dashboard-header">
        <div>
          <h1>Student Analytics Dashboard</h1>
          <p className="subtitle">
            Student Alcohol Consumption · Constellation Data Warehouse
          </p>
        </div>
        <button className="refresh-btn" onClick={refreshAll}>↺ Refresh</button>
      </header>

      {/* ── Gender Distribution ── */}
      <ChartSection
        title="Gender Distribution"
        error={genderError}
        filters={
          <>
            <SchoolFilter  school={genderSchool}   setSchool={setGenderSchool} />
            <SubjectFilter subject={genderSubject} setSubject={setGenderSubject} />
          </>
        }
      >
        <GenderPieChart data={genderData} loading={genderLoading} />
      </ChartSection>

      {/* ── Average Grades ── */}
      <ChartSection
        title="Average Student Grades by Period"
        error={perfError}
        filters={
          <>
            <SchoolFilter  school={perfSchool}   setSchool={setPerfSchool} />
            <SubjectFilter subject={perfSubject} setSubject={setPerfSubject} />
          </>
        }
      >
        <PerformanceBarChart data={perfData} loading={perfLoading} />
      </ChartSection>

      {/* ── Alcohol vs Performance ── */}
      <ChartSection
        title="Alcohol Consumption vs Academic Performance"
        error={alcoholError}
        filters={
          <ConsumptionFilter
            consumptionType={consumptionType}
            setConsumptionType={setConsumptionType}
          />
        }
      >
        <AlcoholPerformanceChart data={alcoholData} loading={alcoholLoading} />
      </ChartSection>

    </div>
  );
};

export default Dashboard;
