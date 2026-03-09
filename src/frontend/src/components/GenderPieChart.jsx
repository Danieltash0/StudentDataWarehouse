import React from 'react';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

const GenderPieChart = ({ data, loading }) => {
  if (loading) {
    return <div className="chart-loading">Loading gender data...</div>;
  }

  if (!data || data.length === 0) {
    return <div className="chart-empty">No gender data available</div>;
  }

  const chartData = data.map(item => ({
    name: item.gender === 'M' ? 'Male' : item.gender === 'F' ? 'Female' : item.gender,
    value: item.total_students
  }));

  return (
    <div className="chart-container">
      <h3>Student Gender Distribution</h3>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

export default GenderPieChart;
