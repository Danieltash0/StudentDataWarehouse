# 📊 Data Warehouse Analytics Dashboard - Complete Project Overview

## 🏗️ Project Architecture

This is a full-stack data warehouse analytics application with three main components:
1. MySQL Data Warehouse (Constellation Schema)
2. ETL Pipeline (Python)
3. REST API Backend (Flask)
4. Interactive Frontend (React + Recharts)

---

## 🗄️ Database Layer

### Database: stud_constellation_dw
- Type: MySQL Database
- Schema: Constellation Schema (Dimension + Fact Tables)

### Dimension Tables 📋
- dim_student: Student demographics (school, sex, age, address, family)
- dim_subject: Academic subjects (Math, Portuguese)
- dim_parent_details: Parent education and job information
- dim_academic_factors: Academic support factors (reason, school support, family support)

### Fact Tables 📈
- fact_student_performance: Academic grades (1st/2nd/final periods, absences)
- fact_student_lifestyle: Lifestyle factors (alcohol consumption, study time, health)

### Database Configuration 🔧
```python
DB_CONFIG = {
    "user": "root",
    "password": "12345", 
    "host": "localhost",
    "port": 3306,
    "database": "stud_constellation_dw"
}
```

---

## ⚙️ ETL Pipeline (src/backend/etl_pipeline/)

### Core Components 🔄

#### extractor.py 📥
- Purpose: Extract raw data from CSV files
- Sources: student-mat.csv, student-por.csv
- Process: Add subject_name column, concatenate datasets

#### transformer.py 🔄
- Purpose: Transform raw data into dimension/fact tables
- Functions:
  - build_dim_student() - Student demographics
  - build_dim_subject() - Subject mapping
  - build_dim_parent_details() - Parent information
  - build_dim_academic_factors() - Academic factors
  - build_fact_student_performance() - Grade data
  - build_fact_student_lifestyle() - Lifestyle data

#### loader.py 📤
- Purpose: Load transformed data into MySQL warehouse
- Features:
  - Generic table loading with deduplication
  - Fact table merging with dimension keys
  - Error handling and logging

#### pipeline.py 🎯
- Purpose: Orchestrate complete ETL process
- Workflow: Extract → Transform → Load
- Database: Creates schema and loads all tables

---

## 🌐 API Backend (src/backend/api/)

### Technology Stack 🛠️
- Framework: Flask 3.1.3
- CORS: Flask-CORS 6.0.2
- Database: SQLAlchemy 2.0.48 + PyMySQL 1.1.2
- Data Processing: Pandas 3.0.1

### API Endpoints 🎯

#### /api/gender-distribution 👥
- Purpose: Gender distribution pie chart data
- Filters: School (GP/MS), Subject (Math/Portuguese)
- SQL: Joins dim_student + fact_student_performance + dim_subject
- Response: [{"gender": "M", "total_students": 123}]

#### /api/performance-grades 📊
- Purpose: Average grades across three periods
- Filters: School, Subject
- SQL: AVG aggregation on first_period_grade, second_period_grade, final_grade
- Response: [{"name": "First Period", "grade": 12.5}]

#### /api/alcohol-performance 🍺
- Purpose: Alcohol consumption vs academic performance correlation
- Filters: Consumption type (weekday/weekend)
- SQL: Joins fact_student_performance + fact_student_lifestyle
- Response: [{"consumption_level": 1, "avg_final_grade": 14.2}]

#### /api/health ✅
- Purpose: API health check and database connectivity
- Response: {"status": "healthy", "database": "connected"}

---

## 🎨 Frontend (src/frontend/)

### Technology Stack 🚀
- Framework: React 19.2.0
- Build Tool: Vite 5.0.8
- Charts: Recharts 2.8.0
- HTTP Client: Axios 1.6.0
- Styling: CSS3 with responsive design

### Component Architecture 🧩

#### Filter Components 🎛️
- SchoolFilter.jsx: School selection (GP/MS)
- SubjectFilter.jsx: Subject selection (Math/Portuguese)  
- ConsumptionFilter.jsx: Alcohol consumption type (weekday/weekend)

#### Chart Components 📈
- GenderPieChart.jsx: Interactive pie chart with gender distribution
- PerformanceBarChart.jsx: Multi-bar chart for academic periods
- AlcoholPerformanceChart.jsx: Correlation bar chart

#### Service Layer 🔌
- api.js: Axios-based API client with base URL http://localhost:5000/api
- Functions: getGenderDistribution(), getPerformanceGrades(), getAlcoholPerformance()

#### Main Components 🎯
- Dashboard.jsx: Main dashboard with independent filter states
- App.jsx: Root component with CSS import
- main.jsx: React entry point

### State Management 🔄
- Independent Filters: Each chart maintains separate filter state
- Real-time Updates: useEffect hooks trigger API calls on filter changes
- Loading States: Individual loading indicators per chart
- Error Handling: Graceful error messages and fallback states

---

## 🎯 Key Features & Capabilities

### Interactive Filtering 🎛️
- School-based filtering: Filter data by GP or MS school
- Subject-based filtering: Filter by Math or Portuguese subjects
- Consumption type filtering: Switch between weekday/weekend alcohol data
- Independent controls: Each chart has its own filter set

### Data Visualization 📊
- Gender Distribution: Pie chart with percentage labels
- Academic Performance: Three-bar comparison chart
- Lifestyle Correlation: Alcohol consumption vs grades analysis
- Responsive Design: Mobile-friendly layout with CSS Grid/Flexbox

### Real-time Updates ⚡
- Dynamic API calls: Filters trigger immediate data refresh
- Loading indicators: Visual feedback during data fetching
- Error handling: User-friendly error messages
- Data validation: Empty state handling

---

## 🔗 System Integration

### Data Flow 🌊
```
CSV Files → ETL Pipeline → MySQL Warehouse → Flask API → React Dashboard
```

### Development Workflow 🛠️
1. ETL: python src/backend/etl_pipeline/pipeline.py
2. Backend: python src/backend/api/app.py (Port 5000)
3. Frontend: npm run dev in src/frontend/ (Port 5173)

### Database Connections 🔌
- ETL Pipeline: Direct MySQL connection for data loading
- API Backend: SQLAlchemy engine with connection pooling
- Frontend: HTTP requests to REST API endpoints

---

## 📁 Project Structure

### Backend Structure (src/backend/)
```
src/backend/
├── api/                          # Flask REST API
│   ├── app.py                   # Main Flask application
│   ├── routes.py                # Route exports
│   └── requirements.txt         # Python dependencies
├── etl_pipeline/                # ETL processing
│   ├── extractor.py            # Data extraction
│   ├── transformer.py          # Data transformation
│   ├── loader.py               # Data loading
│   ├── pipeline.py             # ETL orchestration
│   └── db_config.py            # Database configuration
└── data/                        # Raw data and schemas
    └── database/
        ├── Student_Alc_DB.sql   # Database DDL
        └── analytics_view.sql   # Analytics view
```

### Frontend Structure (src/frontend/)
```
src/frontend/
├── src/
│   ├── components/              # React components
│   │   ├── GenderPieChart.jsx
│   │   ├── PerformanceBarChart.jsx
│   │   ├── AlcoholPerformanceChart.jsx
│   │   ├── SchoolFilter.jsx
│   │   ├── SubjectFilter.jsx
│   │   └── ConsumptionFilter.jsx
│   ├── pages/
│   │   └── Dashboard.jsx        # Main dashboard page
│   ├── services/
│   │   └── api.js               # API service layer
│   ├── App.jsx                  # Root component
│   ├── App.css                  # Dashboard styling
│   └── main.jsx                 # React entry point
├── package.json                 # Dependencies and scripts
├── vite.config.js              # Vite configuration
└── index.html                  # HTML template
```

---

## 🚀 Dependencies

### Backend Dependencies (requirements.txt)
- flask==2.3.0 - Web framework
- flask-cors==4.0.0 - Cross-origin resource sharing
- sqlalchemy==2.0.0 - ORM and database toolkit
- pymysql==1.0.0 - MySQL database connector
- pandas==2.0.0 - Data manipulation library

### Frontend Dependencies (package.json)
- react==^19.2.0 - UI library
- react-dom==^19.2.0 - DOM rendering
- recharts==^2.8.0 - Chart library
- axios==^1.6.0 - HTTP client
- vite==^5.0.8 - Build tool and dev server

---

## 🎯 Usage Instructions

### Setup Database
1. Install MySQL and create database
2. Run Student_Alc_DB.sql to create schema
3. Configure db_config.py with database credentials

### Run ETL Pipeline
```bash
cd src/backend/etl_pipeline
python pipeline.py
```

### Start Backend API
```bash
cd src/backend/api
pip install -r requirements.txt
python app.py
```

### Start Frontend
```bash
cd src/frontend
npm install
npm run dev
```

### Access Dashboard
Open browser to http://localhost:5173

---

This is a complete, production-ready data warehouse analytics system with proper separation of concerns, modern web technologies, and interactive data visualization capabilities!
