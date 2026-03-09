import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from 'recharts';

const PerformanceBarChart = ({ data, loading }) => {
  if (loading) {
    return <div className="chart-loading">Loading performance data...</div>;
  }

  if (!data || data.length === 0) {
    return <div className="chart-empty">No performance data available</div>;
  }

  return (
    <div className="chart-container">
      <h3>Average Student Grades</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis domain={[0, 20]} />
          <Tooltip 
            formatter={(value, name) => [`${parseFloat(value).toFixed(2)}`, 'Average Grade']}
            labelFormatter={(label) => `Period: ${label}`}
          />
          <Bar dataKey="grade" fill="#8884d8" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PerformanceBarChart;
