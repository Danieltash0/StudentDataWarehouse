import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from 'recharts';

const GradesBarChart = ({ data }) => {
  if (!data || data.length === 0) {
    return <div>Loading grade data...</div>;
  }

  return (
    <div className="chart-container">
      <h3>Average Grade by Subject</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="subject_name" />
          <YAxis domain={[0, 20]} />
          <Tooltip 
            formatter={(value, name) => [`${parseFloat(value).toFixed(2)}`, 'Average Grade']}
            labelFormatter={(label) => `Subject: ${label}`}
          />
          <Bar dataKey="avg_grade" fill="#8884d8" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default GradesBarChart;
