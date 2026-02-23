def transform_data(raw_df):
    df = raw_df.copy()

    df.columns = df.columns.str.strip().str.lower()

    # Boolean normalization
    BOOLEAN_COLS = [
        "schoolsup","famsup","paid","activities",
        "nursery","higher","internet","romantic"
    ]

    for col in BOOLEAN_COLS:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.lower()
                .map({"yes": True, "no": False})
                .fillna(False)
            )

    # Enterprise Renaming
    df = df.rename(columns={
        "g1": "first_period_grade",
        "g2": "second_period_grade",
        "g3": "final_grade",
        "medu": "mother_education_level",
        "fedu": "father_education_level",
        "mjob": "mother_job_title",
        "fjob": "father_job_title",
        "dalc": "weekday_alcohol_consumption_level",
        "walc": "weekend_alcohol_consumption_level",
        "famrel": "family_relationship_score",
        "freetime": "free_time_index",
        "goout": "social_activity_index",
        "health": "health_status_score",
        "studytime": "weekly_study_time_category",
        "traveltime": "commute_time_category",
        "failures": "prior_class_failures",
        "absences": "total_absences"
    })

    return df

# Dimensions
def build_dim_student(df):
    cols = [
        "school","sex","age","address",
        "famsize","pstatus","guardian"
    ]
    return df[cols].drop_duplicates().reset_index(drop=True)


def build_dim_subject(df):
    return df[["subject_name"]].drop_duplicates().reset_index(drop=True)


def build_dim_parent_details(df):
    cols = [
        "mother_education_level",
        "father_education_level",
        "mother_job_title",
        "father_job_title"
    ]
    return df[cols].drop_duplicates().reset_index(drop=True)


def build_dim_academic_factors(df):
    cols = ["reason","schoolsup","famsup","paid"]
    return df[cols].drop_duplicates().reset_index(drop=True)


#Facts
def build_fact_student_performance(df):
    cols = [
        "school","sex","age","address","famsize","pstatus","guardian",
        "subject_name",
        "mother_education_level","father_education_level",
        "mother_job_title","father_job_title",
        "reason","schoolsup","famsup","paid",
        "prior_class_failures","total_absences",
        "first_period_grade","second_period_grade","final_grade"
    ]
    return df[cols].copy()


def build_fact_student_lifestyle(df):
    cols = [
        "school","sex","age","address","famsize","pstatus","guardian",
        "commute_time_category",
        "weekly_study_time_category",
        "activities","nursery","higher",
        "internet","romantic",
        "family_relationship_score",
        "free_time_index",
        "social_activity_index",
        "weekday_alcohol_consumption_level",
        "weekend_alcohol_consumption_level",
        "health_status_score"
    ]
    return df[cols].drop_duplicates().copy()
