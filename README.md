# Student Analytics Dashboard

A full-stack analytics dashboard for student performance data with Flask API backend and React frontend, built on a constellation schema data warehouse.

## Architecture Overview

This project implements a **constellation schema** data warehouse with two fact tables connected through shared dimensions:

- **Fact Tables**: `fact_student_performance`, `fact_student_lifestyle`
- **Shared Dimensions**: `dim_student`, `dim_subject`, `dim_parent_details`, `dim_academic_factors`

The constellation schema connects multiple star schemas through common dimension tables, enabling comprehensive analytics across different business domains.

## Project Structure

```
src/
├── backend/
│   ├── data/                    # Data warehouse files
│   │   ├── database/
│   │   │   ├── Student_Alc_DB.sql    # DDL for constellation schema
│   │   │   └── analytics_view.sql    # Analytics view
│   │   └── raw/                     # Raw CSV data
│   ├── etl_pipeline/           # ETL pipeline (unchanged)
│   │   ├── extractor.py
│   │   ├── transformer.py
│   │   ├── loader.py
│   │   ├── pipeline.py
│   │   └── db_config.py
│   └── api/                    # Flask API layer
│       ├── __init__.py
│       ├── app.py             # Main Flask application
│       ├── routes.py          # Route exports
│       └── requirements.txt   # Python dependencies
│
└── frontend/                   # React dashboard
    ├── src/
    │   ├── components/        # Recharts components
    │   │   ├── GenderPieChart.jsx
    │   │   ├── GradesBarChart.jsx
    │   │   └── Filters.jsx
    │   ├── pages/
    │   │   └── Dashboard.jsx   # Main dashboard page
    │   ├── services/
    │   │   └── api.js         # API service layer
    │   ├── App.jsx            # Main React component
    │   └── App.css            # Dashboard styling
    ├── package.json
    └── public/
```

## Setup Instructions

### Prerequisites
- Node.js 20.19+ or 22.12+
- Python 3.8+
- MySQL database with `stud_constellation_dw` database
- ETL pipeline should be run first to populate the database

### 1. Database Setup

1. Create the database schema:
```sql
-- Run src/backend/data/database/Student_Alc_DB.sql
```

2. Run the ETL pipeline to populate data:
```bash
cd src/backend/etl_pipeline
python pipeline.py
```

### 2. Backend API Setup

1. Navigate to the API directory:
```bash
cd src/backend/api
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Start the Flask API server:
```bash
python app.py
```

The API will run on `http://localhost:5000`

### 3. Frontend Dashboard Setup

1. Navigate to the frontend directory:
```bash
cd src/frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Start the React development server:
```bash
npm run dev
```

The dashboard will run on `http://localhost:5173`

## API Endpoints

- `GET /api/gender-distribution` - Student gender distribution
- `GET /api/avg-grade-by-subject?gender=M|F` - Average grades by subject (optional gender filter)
- `GET /api/absences-by-address` - Average absences by address type
- `GET /api/alcohol-vs-performance` - Alcohol consumption vs performance
- `GET /api/health` - API health check

## Dashboard Features

- **Gender Distribution Pie Chart**: Shows student distribution by gender
- **Average Grades Bar Chart**: Displays average final grades by subject
- **Interactive Filters**: Gender and subject filtering capabilities
- **Additional Statistics**: Absences by address and alcohol vs performance data
- **Responsive Design**: Works on desktop and mobile devices

## Data Flow

1. **ETL Pipeline**: Extracts CSV data → Transforms → Loads into constellation schema
2. **Flask API**: Queries the warehouse using SQL joins across fact and dimension tables
3. **React Frontend**: Fetches data via REST API and visualizes with Recharts

## Technology Stack

- **Data Warehouse**: MySQL with constellation schema
- **ETL**: Python with Pandas and SQLAlchemy
- **Backend API**: Flask, SQLAlchemy, Pandas, PyMySQL
- **Frontend**: React, Recharts, Axios, Vite
- **Database Schema**: Constellation schema with connected fact tables

## Constellation Schema Benefits

The constellation schema design enables:
- **Cross-domain analytics**: Performance and lifestyle data analysis
- **Shared dimensions**: Consistent student and subject information across facts
- **Scalability**: Easy addition of new fact tables sharing existing dimensions
- **Data integrity**: Referential integrity through foreign key relationships