import pandas as pd

def transform_data(raw_df):
    df = raw_df.copy()

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    # Handle boolean columns for merged dataset
    BOOLEAN_COLS = [
        "schoolsup.x", "famsup.x", "paid.x", "activities.x",
        "nursery", "higher.x", "internet", "romantic.x"
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

    return df

def build_dim_student(df):
    cols = [
        "school", "sex", "age", "address",
        "famsize", "pstatus", "guardian"
    ]
    return df[cols].drop_duplicates().reset_index(drop=True)

def build_dim_subject(df):
    # Create subject dimension from merged data
    subjects = pd.DataFrame({
        "subject_name": ["Math", "Portuguese"]
    })
    return subjects

def build_dim_parent_details(df):
    cols = [
        "medu", "fedu", "mjob", "fjob"
    ]
    return df[cols].drop_duplicates().reset_index(drop=True)

def build_dim_academic_support(df):
    cols = ["reason", "schoolsup.x", "famsup.x", "paid.x"]
    return df[cols].drop_duplicates().reset_index(drop=True)

def build_fact_student_performance(df):
    """Transform .x and .y columns into separate rows for each subject"""
    performance_rows = []
    
    for _, row in df.iterrows():
        # Math subject record (.x columns)
        math_row = {
            "school": row["school"],
            "sex": row["sex"], 
            "age": row["age"],
            "address": row["address"],
            "famsize": row["famsize"],
            "pstatus": row["pstatus"],
            "guardian": row["guardian"],
            "subject_name": "Math",
            
            "medu": row["medu"],
            "fedu": row["fedu"], 
            "mjob": row["mjob"],
            "fjob": row["fjob"],
            
            "reason": row["reason"],
            "schoolsup": row["schoolsup.x"],
            "famsup": row["famsup.x"],
            "paid": row["paid.x"],
            
            "prior_class_failures": row["failures"],
            "total_absences": row["absences"],
            "weekly_study_time_category": row["studytime"],
            "commute_time_category": row["traveltime"],
            
            "first_period_grade": row["g1.x"],
            "second_period_grade": row["g2.x"], 
            "final_grade": row["g3.x"]
        }
        performance_rows.append(math_row)
        
        # Portuguese subject record (.y columns)
        port_row = {
            "school": row["school"],
            "sex": row["sex"],
            "age": row["age"], 
            "address": row["address"],
            "famsize": row["famsize"],
            "pstatus": row["pstatus"],
            "guardian": row["guardian"],
            "subject_name": "Portuguese",
            
            "medu": row["medu"],
            "fedu": row["fedu"],
            "mjob": row["mjob"],
            "fjob": row["fjob"],
            
            "reason": row["reason"],
            "schoolsup": row["schoolsup.x"],
            "famsup": row["famsup.x"],
            "paid": row["paid.x"],
            
            "prior_class_failures": row["failures"],
            "total_absences": row["absences"],
            "weekly_study_time_category": row["studytime"],
            "commute_time_category": row["traveltime"],
            
            "first_period_grade": row["g1.y"],
            "second_period_grade": row["g2.y"],
            "final_grade": row["g3.y"]
        }
        performance_rows.append(port_row)
    
    return pd.DataFrame(performance_rows)

def build_fact_student_lifestyle(df):
    cols = [
        "school", "sex", "age", "address",
        "famsize", "pstatus", "guardian",

        "commute_time_category",
        "weekly_study_time_category",

        "extracurricular_activities",
        "attended_nursery_school", 
        "plans_higher_education",
        "internet_access",
        "romantic_relationship",

        "family_relationship_quality_score",
        "free_time_index",
        "social_activity_index",
        "weekday_alcohol_consumption_level",
        "weekend_alcohol_consumption_level",
        "health_status_score"
    ]
    
    # Map merged dataset columns to lifestyle fact
    lifestyle_df = pd.DataFrame()
    lifestyle_df["school"] = df["school"]
    lifestyle_df["sex"] = df["sex"]
    lifestyle_df["age"] = df["age"]
    lifestyle_df["address"] = df["address"]
    lifestyle_df["famsize"] = df["famsize"]
    lifestyle_df["pstatus"] = df["pstatus"]
    lifestyle_df["guardian"] = df["guardian"]
    
    lifestyle_df["commute_time_category"] = df["traveltime"]
    lifestyle_df["weekly_study_time_category"] = df["studytime"]
    
    lifestyle_df["extracurricular_activities"] = df["activities.x"]
    lifestyle_df["attended_nursery_school"] = df["nursery"]
    lifestyle_df["plans_higher_education"] = df["higher.x"]
    lifestyle_df["internet_access"] = df["internet"]
    lifestyle_df["romantic_relationship"] = df["romantic.x"]
    
    lifestyle_df["family_relationship_quality_score"] = df["famrel"]
    lifestyle_df["free_time_index"] = df["freetime"]
    lifestyle_df["social_activity_index"] = df["goout"]
    lifestyle_df["weekday_alcohol_consumption_level"] = df["dalc"]
    lifestyle_df["weekend_alcohol_consumption_level"] = df["walc"]
    lifestyle_df["health_status_score"] = df["health"]
    
    return lifestyle_df.drop_duplicates().reset_index(drop=True)
