DROP DATABASE IF EXISTS stud_constellation_dw;
CREATE DATABASE stud_constellation_dw;
USE stud_constellation_dw;

CREATE TABLE dim_student (
    student_key INT AUTO_INCREMENT PRIMARY KEY,
    school VARCHAR(2) NOT NULL,              -- GP, MS
    sex CHAR(1) NOT NULL,                    -- F, M
    age TINYINT NOT NULL,                    -- 15–22
    address CHAR(1),                         -- U, R
    famsize VARCHAR(3),                      -- LE3, GT3
    pstatus CHAR(1),                         -- T, A
    guardian VARCHAR(10)                     -- mother, father, other
);


/* ---------------------------
   dim_parent_education
---------------------------- */
CREATE TABLE dim_parent_education (
    parent_edu_key INT AUTO_INCREMENT PRIMARY KEY,
    Medu TINYINT,
    Fedu TINYINT
);


/* ---------------------------
   dim_parent_job
---------------------------- */
CREATE TABLE dim_parent_job (
    parent_job_key INT AUTO_INCREMENT PRIMARY KEY,
    Mjob VARCHAR(20),
    Fjob VARCHAR(20)
);


/* ---------------------------
   dim_school_reason
---------------------------- */
CREATE TABLE dim_school_reason (
    reason_key INT AUTO_INCREMENT PRIMARY KEY,
    reason VARCHAR(20)   -- home, reputation, course, other
);


/* ---------------------------
   dim_academic_support
---------------------------- */
CREATE TABLE dim_academic_support (
    support_key INT AUTO_INCREMENT PRIMARY KEY,
    schoolsup BOOLEAN,
    famsup BOOLEAN,
    paid BOOLEAN
);


/* ---------------------------
   dim_student_lifestyle
---------------------------- */
CREATE TABLE dim_student_lifestyle (
    lifestyle_key INT AUTO_INCREMENT PRIMARY KEY,
    traveltime TINYINT,
    studytime TINYINT,
    failures TINYINT,
    activities BOOLEAN,
    nursery BOOLEAN,
    higher BOOLEAN,
    internet BOOLEAN,
    romantic BOOLEAN
);


/* ---------------------------
   dim_behavior_health
---------------------------- */
CREATE TABLE dim_behavior_health (
    behavior_key INT AUTO_INCREMENT PRIMARY KEY,
    famrel TINYINT,
    freetime TINYINT,
    goout TINYINT,
    Dalc TINYINT,
    Walc TINYINT,
    health TINYINT
);


/* ---------------------------
   dim_subject
---------------------------- */
CREATE TABLE dim_subject (
    subject_key INT AUTO_INCREMENT PRIMARY KEY,
    subject_name VARCHAR(20)  -- Math, Portuguese
);




CREATE TABLE fact_student_performance (
    performance_key INT AUTO_INCREMENT PRIMARY KEY,

    student_key INT NOT NULL,
    subject_key INT NOT NULL,
    parent_edu_key INT,
    parent_job_key INT,
    reason_key INT,
    support_key INT,

    G1 TINYINT,
    G2 TINYINT,
    G3 TINYINT,

    FOREIGN KEY (student_key) REFERENCES dim_student(student_key),
    FOREIGN KEY (subject_key) REFERENCES dim_subject(subject_key),
    FOREIGN KEY (parent_edu_key) REFERENCES dim_parent_education(parent_edu_key),
    FOREIGN KEY (parent_job_key) REFERENCES dim_parent_job(parent_job_key),
    FOREIGN KEY (reason_key) REFERENCES dim_school_reason(reason_key),
    FOREIGN KEY (support_key) REFERENCES dim_academic_support(support_key)
);


CREATE TABLE fact_student_lifestyle (
    lifestyle_fact_key INT AUTO_INCREMENT PRIMARY KEY,

    student_key INT NOT NULL,
    lifestyle_key INT,
    behavior_key INT,

    absences INT,

    FOREIGN KEY (student_key) REFERENCES dim_student(student_key),
    FOREIGN KEY (lifestyle_key) REFERENCES dim_student_lifestyle(lifestyle_key),
    FOREIGN KEY (behavior_key) REFERENCES dim_behavior_health(behavior_key)
);
