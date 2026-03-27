from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
from sqlalchemy import create_engine, text
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from etl_pipeline.db_config import DB_CONFIG

app = Flask(__name__)

# Allow requests from the nginx frontend container (port 3000)
# and from localhost during local development
CORS(app, resources={r"/api/*": {"origins": [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",   # Vite dev server
]}})

MYSQL_URL = (
    f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
    f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)
engine = create_engine(MYSQL_URL, echo=False, pool_pre_ping=True)


# ── Health check ─────────────────────────────────────────────────────────────
@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return jsonify({'status': 'healthy', 'database': 'connected'}), 200
    except Exception as e:
        # Return 200 anyway so the container doesn't restart in a crash-loop,
        # but surface the error for debugging
        return jsonify({'status': 'degraded', 'database': str(e)}), 200


# ── Gender distribution ───────────────────────────────────────────────────────
@app.route('/api/gender-distribution', methods=['GET'])
def gender_distribution():
    try:
        school  = request.args.get('school')
        subject = request.args.get('subject')

        query = """
            SELECT
                d.sex          AS gender,
                COUNT(DISTINCT d.student_id) AS total_students,
                d.school,
                s.subject_name AS subject
            FROM dim_student d
            JOIN fact_student_performance f ON d.student_id = f.student_id
            JOIN dim_subject s              ON f.subject_id = s.subject_id
            WHERE 1=1
        """
        params = []
        if school:
            query += " AND d.school = %s"
            params.append(school)
        if subject:
            query += " AND s.subject_name = %s"
            params.append(subject)

        query += " GROUP BY d.sex, d.school, s.subject_name"

        df = pd.read_sql(query, engine, params=params if params else None)
        return jsonify(df.to_dict('records')), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── Average grades ────────────────────────────────────────────────────────────
@app.route('/api/average-grades', methods=['GET'])
def average_grades():
    try:
        school  = request.args.get('school')
        subject = request.args.get('subject')

        query = """
            SELECT
                AVG(f.first_period_grade)  AS avg_first_period_grade,
                AVG(f.second_period_grade) AS avg_second_period_grade,
                AVG(f.final_grade)         AS avg_final_grade
            FROM fact_student_performance f
            JOIN dim_student d ON f.student_id = d.student_id
            JOIN dim_subject s ON f.subject_id = s.subject_id
            WHERE 1=1
        """
        params = []
        if school:
            query += " AND d.school = %s"
            params.append(school)
        if subject:
            query += " AND s.subject_name = %s"
            params.append(subject)

        df = pd.read_sql(query, engine, params=params if params else None)

        if df.empty or df['avg_final_grade'].isnull().all():
            return jsonify([]), 200

        result = [
            {'name': 'First Period',  'grade': round(float(df['avg_first_period_grade'].iloc[0]),  2)},
            {'name': 'Second Period', 'grade': round(float(df['avg_second_period_grade'].iloc[0]), 2)},
            {'name': 'Final Grade',   'grade': round(float(df['avg_final_grade'].iloc[0]),         2)},
        ]
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── Alcohol vs performance ────────────────────────────────────────────────────
@app.route('/api/alcohol-vs-performance', methods=['GET'])
def alcohol_vs_performance():
    try:
        consumption_type = request.args.get(
            'consumption_level_type', 'weekend_alcohol_consumption_level'
        )

        # Whitelist to prevent SQL injection via the column name
        valid = {
            'weekday_alcohol_consumption_level',
            'weekend_alcohol_consumption_level',
        }
        if consumption_type not in valid:
            consumption_type = 'weekend_alcohol_consumption_level'

        query = f"""
            SELECT
                l.{consumption_type}  AS consumption_level,
                ROUND(AVG(p.final_grade), 2) AS avg_final_grade
            FROM fact_student_performance p
            JOIN fact_student_lifestyle l ON p.student_id = l.student_id
            GROUP BY l.{consumption_type}
            ORDER BY l.{consumption_type}
        """

        df = pd.read_sql(query, engine)
        return jsonify(df.to_dict('records')), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
