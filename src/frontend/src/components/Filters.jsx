import React from 'react';

const Filters = ({ gender, setGender, subject, setSubject }) => {
  return (
    <div className="filters-container">
      <h3>Filters</h3>
      <div className="filter-group">
        <label htmlFor="gender-filter">Gender:</label>
        <select 
          id="gender-filter"
          value={gender} 
          onChange={(e) => setGender(e.target.value)}
        >
          <option value="">All</option>
          <option value="M">Male</option>
          <option value="F">Female</option>
        </select>
      </div>
      
      <div className="filter-group">
        <label htmlFor="subject-filter">Subject:</label>
        <select 
          id="subject-filter"
          value={subject} 
          onChange={(e) => setSubject(e.target.value)}
        >
          <option value="">All</option>
          <option value="Math">Math</option>
          <option value="Portuguese">Portuguese</option>
        </select>
      </div>
    </div>
  );
};

export default Filters;
