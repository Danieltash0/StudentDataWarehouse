from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
from sqlalchemy import create_engine
import sys
import os

# Add parent directory to path to import db_config
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from etl_pipeline.db_config import DB_CONFIG

app = Flask(__name__)
CORS(app)

# Database connection
MYSQL_URL = (
    f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
    f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)
engine = create_engine(MYSQL_URL, echo=False, pool_pre_ping=True)

@app.route('/api/gender-distribution', methods=['GET'])
def gender_distribution():
    try:
        school = request.args.get('school')
        subject = request.args.get('subject')
        
        query = """
        SELECT
        d.sex AS gender,
        COUNT(*) AS total_students
        FROM dim_student d
        JOIN fact_student_performance f
        ON d.student_id = f.student_id
        JOIN dim_subject s
        ON f.subject_id = s.subject_id
        WHERE 1=1
        """
        
        params = []
        if school:
            query += " AND d.school = %s"
            params.append(school)
        if subject:
            query += " AND s.subject_name = %s"
            params.append(subject)
            
        query += " GROUP BY d.sex"
        
        df = pd.read_sql(query, engine, params=params)
        return jsonify(df.to_dict('records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/performance-grades', methods=['GET'])
def performance_grades():
    try:
        school = request.args.get('school')
        subject = request.args.get('subject')
        
        query = """
        SELECT
        AVG(f.first_period_grade) AS avg_first_grade,
        AVG(f.second_period_grade) AS avg_second_grade,
        AVG(f.final_grade) AS avg_final_grade
        FROM fact_student_performance f
        JOIN dim_student d
        ON f.student_id = d.student_id
        JOIN dim_subject s
        ON f.subject_id = s.subject_id
        WHERE 1=1
        """
        
        params = []
        if school:
            query += " AND d.school = %s"
            params.append(school)
        if subject:
            query += " AND s.subject_name = %s"
            params.append(subject)
            
        df = pd.read_sql(query, engine, params=params)
        
        # Transform data for Recharts format
        result = [
            {'name': 'First Period', 'grade': float(df['avg_first_grade'].iloc[0]) if not df.empty else 0},
            {'name': 'Second Period', 'grade': float(df['avg_second_grade'].iloc[0]) if not df.empty else 0},
            {'name': 'Final Grade', 'grade': float(df['avg_final_grade'].iloc[0]) if not df.empty else 0}
        ]
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/absences-by-address', methods=['GET'])
def absences_by_address():
    try:
        query = """
        SELECT d.address, AVG(f.total_absences) AS avg_absences
        FROM fact_student_performance f
        JOIN dim_student d ON f.student_id = d.student_id
        GROUP BY d.address
        """
        df = pd.read_sql(query, engine)
        return jsonify(df.to_dict('records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/alcohol-performance', methods=['GET'])
def alcohol_performance():
    try:
        consumption_type = request.args.get('consumption_type', 'weekend')
        
        if consumption_type == 'weekday':
            query = """
            SELECT
            l.weekday_alcohol_consumption_level AS consumption_level,
            AVG(p.final_grade) AS avg_final_grade
            FROM fact_student_performance p
            JOIN fact_student_lifestyle l
            ON p.student_id = l.student_id
            GROUP BY l.weekday_alcohol_consumption_level
            ORDER BY l.weekday_alcohol_consumption_level
            """
        else:  # default to weekend
            query = """
            SELECT
            l.weekend_alcohol_consumption_level AS consumption_level,
            AVG(p.final_grade) AS avg_final_grade
            FROM fact_student_performance p
            JOIN fact_student_lifestyle l
            ON p.student_id = l.student_id
            GROUP BY l.weekend_alcohol_consumption_level
            ORDER BY l.weekend_alcohol_consumption_level
            """
        
        df = pd.read_sql(query, engine)
        return jsonify(df.to_dict('records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'database': 'connected'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
