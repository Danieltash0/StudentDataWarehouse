import React from 'react';

const ConsumptionFilter = ({ consumptionType, setConsumptionType }) => (
  <div className="filter-group">
    <label htmlFor="consumption-filter">Consumption Period</label>
    <select
      id="consumption-filter"
      value={consumptionType}
      onChange={(e) => setConsumptionType(e.target.value)}
    >
      <option value="weekend_alcohol_consumption_level">Weekend</option>
      <option value="weekday_alcohol_consumption_level">Weekday</option>
    </select>
  </div>
);

export default ConsumptionFilter;
