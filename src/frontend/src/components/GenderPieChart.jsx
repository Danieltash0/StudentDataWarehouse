import React from 'react';
import {
  PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer,
} from 'recharts';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

const GenderPieChart = ({ data, loading }) => {
  if (loading) return <div className="chart-placeholder">Loading gender data...</div>;
  if (!data || data.length === 0) return <div className="chart-placeholder">No data available</div>;

  // BUG FIX: The API can return multiple rows for the same gender when no
  // school/subject filter is active (one row per school × subject combo).
  // Aggregate total_students by gender before passing to Recharts.
  const aggregated = data.reduce((acc, item) => {
    const key = item.gender === 'M' ? 'Male' : item.gender === 'F' ? 'Female' : item.gender;
    acc[key] = (acc[key] || 0) + Number(item.total_students);
    return acc;
  }, {});

  const chartData = Object.entries(aggregated).map(([name, value]) => ({ name, value }));

  return (
    <div className="chart-container">
      <ResponsiveContainer width="100%" height={320}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            outerRadius={110}
            dataKey="value"
            labelLine={false}
            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
          >
            {chartData.map((_, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip formatter={(value) => [value, 'Students']} />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

export default GenderPieChart;
