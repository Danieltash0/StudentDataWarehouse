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
        <option value="weekend_alcohol_consumption_level">Weekend Alcohol Consumption</option>
        <option value="weekday_alcohol_consumption_level">Weekday Alcohol Consumption</option>
      </select>
    </div>
  );
};

export default ConsumptionFilter;
