import React from 'react';

const ConsumptionFilter = ({ consumptionType, setConsumptionType }) => {
  return (
    <div className="filter-group">
      <label htmlFor="consumption-filter">Consumption Type:</label>
      <select 
        id="consumption-filter"
        value={consumptionType} 
        onChange={(e) => setConsumptionType(e.target.value)}
      >
        <option value="weekend">Weekend Alcohol Consumption</option>
        <option value="weekday">Weekday Alcohol Consumption</option>
      </select>
    </div>
  );
};

export default ConsumptionFilter;
