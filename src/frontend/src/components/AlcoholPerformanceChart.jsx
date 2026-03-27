import React from 'react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid,
  ResponsiveContainer, Cell, ReferenceLine,
} from 'recharts';

// 5-stop gradient: green (level 1) → red (level 5)
const LEVEL_COLORS = ['#22c55e', '#84cc16', '#eab308', '#f97316', '#ef4444'];

const LEVEL_LABELS = { 1: 'Very Low', 2: 'Low', 3: 'Moderate', 4: 'High', 5: 'Very High' };

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{ background: '#fff', border: '1px solid #e5e7eb', borderRadius: 8, padding: '10px 14px' }}>
      <p style={{ margin: 0, fontWeight: 600 }}>Level {label} — {LEVEL_LABELS[label] || ''}</p>
      <p style={{ margin: '4px 0 0', color: '#6366f1' }}>
        Avg Final Grade: <strong>{parseFloat(payload[0].value).toFixed(2)}</strong> / 20
      </p>
    </div>
  );
};

const AlcoholPerformanceChart = ({ data, loading }) => {
  if (loading) return <div className="chart-placeholder">Loading alcohol data...</div>;
  if (!data || data.length === 0) return <div className="chart-placeholder">No data available</div>;

  // Overall average line
  const avgGrade = data.reduce((s, d) => s + Number(d.avg_final_grade), 0) / data.length;

  return (
    <div className="chart-container">
      <ResponsiveContainer width="100%" height={320}>
        <BarChart data={data} margin={{ top: 24, right: 30, left: 10, bottom: 20 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis
            dataKey="consumption_level"
            label={{ value: 'Alcohol Consumption Level (1 = lowest, 5 = highest)', position: 'insideBottom', offset: -12, fill: '#888', fontSize: 12 }}
            tick={{ fill: '#555' }}
          />
          <YAxis
            domain={[0, 20]}
            tick={{ fill: '#555' }}
            label={{ value: 'Avg Final Grade /20', angle: -90, position: 'insideLeft', fill: '#888', fontSize: 12 }}
          />
          <Tooltip content={<CustomTooltip />} />
          <ReferenceLine y={avgGrade} stroke="#94a3b8" strokeDasharray="4 4"
            label={{ value: `Overall avg ${avgGrade.toFixed(1)}`, position: 'right', fill: '#94a3b8', fontSize: 11 }} />
          <Bar dataKey="avg_final_grade" radius={[6, 6, 0, 0]}>
            {data.map((entry, index) => (
              <Cell
                key={index}
                fill={LEVEL_COLORS[(entry.consumption_level - 1) % LEVEL_COLORS.length]}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default AlcoholPerformanceChart;
