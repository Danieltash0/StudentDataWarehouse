CREATE DATABASE stud_constellation_dw;
USE stud_constellation_dw;


CREATE TABLE dim_student (
    student_ID INT AUTO_INCREMENT PRIMARY KEY,
    school VARCHAR(2) NOT NULL,
    sex CHAR(1) NOT NULL,
    age TINYINT NOT NULL,
    address CHAR(1),
    famsize VARCHAR(3),
    pstatus CHAR(1),
    guardian VARCHAR(10)
);

CREATE TABLE dim_subject (
    subject_ID INT AUTO_INCREMENT PRIMARY KEY,
    subject_name VARCHAR(20) NOT NULL
);

CREATE TABLE dim_parent_details (
    parent_details_ID INT AUTO_INCREMENT PRIMARY KEY,
    Medu TINYINT,
    Fedu TINYINT,
    Mjob VARCHAR(20),
    Fjob VARCHAR(20)
);

CREATE TABLE dim_academic_factors (
    academic_factors_ID INT AUTO_INCREMENT PRIMARY KEY,
    reason VARCHAR(20),
    schoolsup BOOLEAN,
    famsup BOOLEAN,
    paid BOOLEAN
);

CREATE TABLE fact_student_performance (
    performance_ID INT AUTO_INCREMENT PRIMARY KEY,

    student_ID INT NOT NULL,
    subject_ID INT NOT NULL,
    parent_details_ID INT,
    academic_factors_ID INT,

    G1 TINYINT,
    G2 TINYINT,
    G3 TINYINT,

    failures TINYINT,
    absences INT,

    FOREIGN KEY (student_ID)
        REFERENCES dim_student(student_ID),

    FOREIGN KEY (subject_ID)
        REFERENCES dim_subject(subject_ID),

    FOREIGN KEY (parent_details_ID)
        REFERENCES dim_parent_details(parent_details_ID),

    FOREIGN KEY (academic_factors_ID)
        REFERENCES dim_academic_factors(academic_factors_ID)
);

CREATE TABLE fact_student_lifestyle (
    lifestyle_ID INT AUTO_INCREMENT PRIMARY KEY,

    student_ID INT NOT NULL,

    traveltime TINYINT,
    studytime TINYINT,
    activities BOOLEAN,
    nursery BOOLEAN,
    higher BOOLEAN,
    internet BOOLEAN,
    romantic BOOLEAN,

    famrel TINYINT,
    freetime TINYINT,
    goout TINYINT,
    Dalc TINYINT,
    Walc TINYINT,
    health TINYINT,

    FOREIGN KEY (student_ID)
        REFERENCES dim_student(student_ID)
);
