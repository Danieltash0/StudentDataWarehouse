import React from 'react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid,
  ResponsiveContainer, Cell, LabelList,
} from 'recharts';

const PERIOD_COLORS = ['#6366f1', '#8b5cf6', '#a855f7'];

const PerformanceBarChart = ({ data, loading }) => {
  if (loading) return <div className="chart-placeholder">Loading grade data...</div>;
  if (!data || data.length === 0) return <div className="chart-placeholder">No grade data available</div>;

  return (
    <div className="chart-container">
      <ResponsiveContainer width="100%" height={320}>
        <BarChart data={data} margin={{ top: 24, right: 30, left: 10, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis dataKey="name" tick={{ fill: '#555' }} />
          <YAxis domain={[0, 20]} tick={{ fill: '#555' }} label={{ value: 'Grade /20', angle: -90, position: 'insideLeft', fill: '#888', fontSize: 12 }} />
          <Tooltip
            formatter={(value) => [parseFloat(value).toFixed(2), 'Avg Grade']}
            labelFormatter={(label) => `Period: ${label}`}
            contentStyle={{ borderRadius: 8 }}
          />
          <Bar dataKey="grade" radius={[6, 6, 0, 0]}>
            {data.map((_, index) => (
              <Cell key={index} fill={PERIOD_COLORS[index % PERIOD_COLORS.length]} />
            ))}
            <LabelList dataKey="grade" position="top" formatter={(v) => parseFloat(v).toFixed(1)} style={{ fontSize: 12, fill: '#555' }} />
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PerformanceBarChart;
