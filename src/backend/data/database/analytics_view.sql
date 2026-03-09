USE stud_constellation_dw;

CREATE OR REPLACE VIEW vw_student_analytics AS
SELECT
    -- STUDENT INFORMATION

    ds.school,
    ds.sex,
    ds.age,
    ds.address,
    ds.famsize,
    ds.pstatus,
    ds.guardian,

    -- SUBJECT
    subj.subject_name,

    -- PARENT DETAILS
    pd.mother_education_level,
    pd.father_education_level,
    pd.mother_job_title,
    pd.father_job_title,

    -- ACADEMIC FACTORS (BOOLEAN DISPLAY FIX)
    af.reason,

    CASE WHEN af.schoolsup = 1 THEN 'Yes' ELSE 'No' END AS school_support,
    CASE WHEN af.famsup = 1 THEN 'Yes' ELSE 'No' END AS family_support,
    CASE WHEN af.paid = 1 THEN 'Yes' ELSE 'No' END AS extra_paid_classes,

    -- PERFORMANCE METRICS
    fp.first_period_grade,
    fp.second_period_grade,
    fp.final_grade,
    fp.prior_class_failures,
    fp.total_absences,

    -- LIFESTYLE METRICS
    fl.commute_time_category,
    fl.weekly_study_time_category,

    CASE WHEN fl.activities = 1 THEN 'Yes' ELSE 'No' END AS extracurricular_activities,
    CASE WHEN fl.nursery = 1 THEN 'Yes' ELSE 'No' END AS attended_nursery,
    CASE WHEN fl.higher = 1 THEN 'Yes' ELSE 'No' END AS wants_higher_education,
    CASE WHEN fl.internet = 1 THEN 'Yes' ELSE 'No' END AS has_internet_access,
    CASE WHEN fl.romantic = 1 THEN 'Yes' ELSE 'No' END AS in_romantic_relationship,

    fl.family_relationship_score,
    fl.free_time_index,
    fl.social_activity_index,
    fl.weekday_alcohol_consumption_level,
    fl.weekend_alcohol_consumption_level,
    fl.health_status_score

FROM fact_student_performance fp

JOIN dim_student ds
    ON fp.student_id = ds.student_id

JOIN dim_subject subj
    ON fp.subject_id = subj.subject_id

LEFT JOIN dim_parent_details pd
    ON fp.parent_details_id = pd.parent_details_id

LEFT JOIN dim_academic_factors af
    ON fp.academic_factors_id = af.academic_factors_id

LEFT JOIN fact_student_lifestyle fl
    ON ds.student_id = fl.student_id;
