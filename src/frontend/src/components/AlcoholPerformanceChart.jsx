import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from 'recharts';

const AlcoholPerformanceChart = ({ data, loading }) => {
  if (loading) {
    return <div className="chart-loading">Loading alcohol performance data...</div>;
  }

  if (!data || data.length === 0) {
    return <div className="chart-empty">No alcohol performance data available</div>;
  }

  return (
    <div className="chart-container">
      <h3>Alcohol Consumption vs Academic Performance</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="consumption_level" 
            label={{ value: 'Alcohol Consumption Level', position: 'insideBottom', offset: -5 }}
          />
          <YAxis 
            domain={[0, 20]} 
            label={{ value: 'Average Final Grade', angle: -90, position: 'insideLeft' }}
          />
          <Tooltip 
            formatter={(value, name) => [`${parseFloat(value).toFixed(2)}`, 'Avg Final Grade']}
            labelFormatter={(label) => `Consumption Level: ${label}`}
          />
          <Bar dataKey="avg_final_grade" fill="#82ca9d" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default AlcoholPerformanceChart;
