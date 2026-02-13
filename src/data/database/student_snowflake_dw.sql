CREATE DATABASE student_snowflake_dw;
USE student_snowflake_dw;

CREATE TABLE dim_parent_education (
    parent_edu_id INT AUTO_INCREMENT PRIMARY KEY,
    Medu TINYINT,
    Fedu TINYINT
) ENGINE=InnoDB;

CREATE TABLE dim_parent_job (
    parent_job_id INT AUTO_INCREMENT PRIMARY KEY,
    Mjob VARCHAR(50),
    Fjob VARCHAR(50)
) ENGINE=InnoDB;

CREATE TABLE dim_location (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    address VARCHAR(50)
) ENGINE=InnoDB;

CREATE TABLE dim_guardian (
    guardian_id INT AUTO_INCREMENT PRIMARY KEY,
    guardian_type VARCHAR(50)
) ENGINE=InnoDB;

CREATE TABLE dim_region (
    region_id INT AUTO_INCREMENT PRIMARY KEY,
    region_name VARCHAR(100)
) ENGINE=InnoDB;

CREATE TABLE dim_subject (
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_name VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE dim_school (
    school_id INT AUTO_INCREMENT PRIMARY KEY,
    school_code VARCHAR(10),
    region_id INT,
    FOREIGN KEY (region_id)
        REFERENCES dim_region(region_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE dim_family (
    family_id INT AUTO_INCREMENT PRIMARY KEY,
    famsize VARCHAR(10),
    Pstatus VARCHAR(10),
    famrel TINYINT,
    parent_edu_id INT,
    parent_job_id INT,
    FOREIGN KEY (parent_edu_id)
        REFERENCES dim_parent_education(parent_edu_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    FOREIGN KEY (parent_job_id)
        REFERENCES dim_parent_job(parent_job_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE dim_student (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    sex VARCHAR(10),
    age TINYINT,
    internet VARCHAR(10),
    higher VARCHAR(10),
    romantic VARCHAR(10),
    location_id INT,
    guardian_id INT,
    FOREIGN KEY (location_id)
        REFERENCES dim_location(location_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    FOREIGN KEY (guardian_id)
        REFERENCES dim_guardian(guardian_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE fact_student_performance (
    performance_id INT AUTO_INCREMENT PRIMARY KEY,

    student_id INT NOT NULL,
    family_id INT NOT NULL,
    school_id INT NOT NULL,
    subject_id INT NOT NULL,

    traveltime TINYINT,
    studytime TINYINT,
    failures TINYINT,
    freetime TINYINT,
    goout TINYINT,
    dalc TINYINT,
    walc TINYINT,
    health TINYINT,
    absences INT,

    g1 TINYINT,
    g2 TINYINT,
    g3 TINYINT,

    FOREIGN KEY (student_id)
        REFERENCES dim_student(student_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (family_id)
        REFERENCES dim_family(family_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (school_id)
        REFERENCES dim_school(school_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (subject_id)
        REFERENCES dim_subject(subject_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE INDEX idx_fact_student ON fact_student_performance(student_id);
CREATE INDEX idx_fact_family ON fact_student_performance(family_id);
CREATE INDEX idx_fact_school ON fact_student_performance(school_id);
CREATE INDEX idx_fact_subject ON fact_student_performance(subject_id);

