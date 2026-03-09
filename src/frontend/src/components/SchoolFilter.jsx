import React from 'react';

const SchoolFilter = ({ school, setSchool }) => {
  return (
    <div className="filter-group">
      <label htmlFor="school-filter">School:</label>
      <select 
        id="school-filter"
        value={school} 
        onChange={(e) => setSchool(e.target.value)}
      >
        <option value="">All Schools</option>
        <option value="GP">GP - Gabriel Pereira</option>
        <option value="MS">MS - Mousinho da Silveira</option>
      </select>
    </div>
  );
};

export default SchoolFilter;
