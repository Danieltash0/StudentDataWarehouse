CREATE DATABASE stud_constellation_dw;
USE stud_constellation_dw;

-- =========================
-- DIMENSIONS
-- =========================

CREATE TABLE dim_student (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    school VARCHAR(2) NOT NULL,
    sex CHAR(1) NOT NULL,
    age TINYINT NOT NULL,
    address CHAR(1),
    famsize VARCHAR(3),
    pstatus CHAR(1),
    guardian VARCHAR(10)
);

CREATE TABLE dim_subject (
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_name VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE dim_parent_details (
    parent_details_id INT AUTO_INCREMENT PRIMARY KEY,
    mother_education_level TINYINT,
    father_education_level TINYINT,
    mother_job_title VARCHAR(20),
    father_job_title VARCHAR(20)
);

CREATE TABLE dim_academic_factors (
    academic_factors_id INT AUTO_INCREMENT PRIMARY KEY,
    reason VARCHAR(20),
    schoolsup BOOLEAN,
    famsup BOOLEAN,
    paid BOOLEAN
);

-- =========================
-- FACT TABLES
-- =========================

CREATE TABLE fact_student_performance (
    performance_id INT AUTO_INCREMENT PRIMARY KEY,

    student_id INT NOT NULL,
    subject_id INT NOT NULL,
    parent_details_id INT,
    academic_factors_id INT,

    first_period_grade TINYINT,
    second_period_grade TINYINT,
    final_grade TINYINT,

    prior_class_failures TINYINT,
    total_absences INT,

    FOREIGN KEY (student_id)
        REFERENCES dim_student(student_id),

    FOREIGN KEY (subject_id)
        REFERENCES dim_subject(subject_id),

    FOREIGN KEY (parent_details_id)
        REFERENCES dim_parent_details(parent_details_id),

    FOREIGN KEY (academic_factors_id)
        REFERENCES dim_academic_factors(academic_factors_id)
);

CREATE TABLE fact_student_lifestyle (
    lifestyle_id INT AUTO_INCREMENT PRIMARY KEY,

    student_id INT NOT NULL,

    commute_time_category TINYINT,
    weekly_study_time_category TINYINT,

    activities BOOLEAN,
    nursery BOOLEAN,
    higher BOOLEAN,
    internet BOOLEAN,
    romantic BOOLEAN,

    family_relationship_score TINYINT,
    free_time_index TINYINT,
    social_activity_index TINYINT,
    weekday_alcohol_consumption_level TINYINT,
    weekend_alcohol_consumption_level TINYINT,
    health_status_score TINYINT,

    FOREIGN KEY (student_id)
        REFERENCES dim_student(student_id)
);
