import React from 'react';

const SubjectFilter = ({ subject, setSubject }) => {
  return (
    <div className="filter-group">
      <label htmlFor="subject-filter">Subject:</label>
      <select 
        id="subject-filter"
        value={subject} 
        onChange={(e) => setSubject(e.target.value)}
      >
        <option value="">All Subjects</option>
        <option value="Math">Math</option>
        <option value="Portuguese">Portuguese</option>
      </select>
    </div>
  );
};

export default SubjectFilter;
