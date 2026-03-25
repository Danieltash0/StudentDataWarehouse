CREATE DATABASE IF NOT EXISTS stud_constellation_dw;
USE stud_constellation_dw;

-- DIMENSIONS

CREATE TABLE IF NOT EXISTS dim_student (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    school VARCHAR(2) NOT NULL,
    sex CHAR(1) NOT NULL,
    age TINYINT NOT NULL,
    address VARCHAR(10),
    family_size VARCHAR(3),
    parent_cohabitation_status CHAR(1),
    guardian VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS dim_subject (
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_name VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS dim_parent_details (
    parent_details_id INT AUTO_INCREMENT PRIMARY KEY,
    mother_education_level TINYINT,
    father_education_level TINYINT,
    mother_job_title VARCHAR(20),
    father_job_title VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS dim_academic_support (
    academic_support_id INT AUTO_INCREMENT PRIMARY KEY,
    school_support BOOLEAN,
    family_support BOOLEAN,
    extra_paid_classes BOOLEAN,
    school_choice_reason VARCHAR(20)
);

-- FACT TABLES

CREATE TABLE IF NOT EXISTS fact_student_performance (
    performance_id INT AUTO_INCREMENT PRIMARY KEY,

    student_id INT NOT NULL,
    subject_id INT NOT NULL,
    parent_details_id INT,
    academic_support_id INT,

    first_period_grade TINYINT,
    second_period_grade TINYINT,
    final_grade TINYINT,

    prior_class_failures TINYINT,
    total_absences INT,
    weekly_study_time_category TINYINT,
    commute_time_category TINYINT,

    FOREIGN KEY (student_id)
        REFERENCES dim_student(student_id),

    FOREIGN KEY (subject_id)
        REFERENCES dim_subject(subject_id),

    FOREIGN KEY (parent_details_id)
        REFERENCES dim_parent_details(parent_details_id),

    FOREIGN KEY (academic_support_id)
        REFERENCES dim_academic_support(academic_support_id)
);

CREATE TABLE IF NOT EXISTS fact_student_lifestyle (
    lifestyle_id INT AUTO_INCREMENT PRIMARY KEY,

    student_id INT NOT NULL,

    extracurricular_activities BOOLEAN,
    attended_nursery_school BOOLEAN,
    plans_higher_education BOOLEAN,
    internet_access BOOLEAN,
    romantic_relationship BOOLEAN,

    family_relationship_quality_score TINYINT,
    free_time_index TINYINT,
    social_activity_index TINYINT,
    weekday_alcohol_consumption_level TINYINT,
    weekend_alcohol_consumption_level TINYINT,
    health_status_score TINYINT,

    FOREIGN KEY (student_id)
        REFERENCES dim_student(student_id)
);
