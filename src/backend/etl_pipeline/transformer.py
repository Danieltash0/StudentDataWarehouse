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
    """
    Build student dimension.

    DESIGN NOTE: The 7-column composite key (school, sex, age, address,
    family_size, pstatus, guardian) is NOT unique per student — 382 students
    collapse to only 112 distinct combos. Even all 13 R merge keys only yield
    366 unique combos. Therefore we use the DataFrame row index (0..381) as a
    stable surrogate key, inserting an explicit 'student_id' (1-based) so that
    fact tables can reference it without a brittle composite-key lookup.
    """
    # Helper to find column (case-insensitive, strips quotes)
    def find_col(name):
        for col in df.columns:
            if col.replace('"', '').strip().lower() == name.lower():
                return col
        return None

    # BUG FIX: merged dataset splits 'guardian' into 'guardian.x'/'guardian.y'
    # Use 'guardian.x' as the guardian column
    cols_map = {
        'school': find_col('school'),
        'sex': find_col('sex'),
        'age': find_col('age'),
        'address': find_col('address'),
        'family_size': find_col('famsize'),
        'parent_cohabitation_status': find_col('pstatus'),
        'guardian': find_col('guardian.x'),  # Use guardian.x instead of guardian
    }

    missing = [k for k, v in cols_map.items() if v is None]
    if missing:
        # If guardian.x not found, try guardian
        if 'guardian' in missing:
            guardian_col = find_col('guardian')
            if guardian_col:
                cols_map['guardian'] = guardian_col
                missing.remove('guardian')
        
        if missing:
            raise ValueError(f"Required student columns not found: {missing}")

    # Build DataFrame with found columns only
    student_df = pd.DataFrame({k: df[v].values for k, v in cols_map.items()})

    # Add explicit 1-based surrogate key so fact tables can reference it directly
    student_df.insert(0, 'student_id', range(1, len(student_df) + 1))

    # Do NOT drop_duplicates — each row IS a distinct student (382 rows required)
    return student_df.reset_index(drop=True)

def build_dim_subject(df):
    """Create subject dimension with Math and Portuguese"""
    return pd.DataFrame({"subject_name": ["Math", "Portuguese"]})

def build_dim_parent_details(df):
    """Build parent details dimension with deduplication"""
    def find_col(name):
        for col in df.columns:
            if col.replace('"', '').strip().lower() == name.lower():
                return col
        return None

    parent_df = pd.DataFrame({
        'mother_education_level': df[find_col('medu')].values,
        'father_education_level': df[find_col('fedu')].values,
        'mother_job_title': df[find_col('mjob')].values,
        'father_job_title': df[find_col('fjob')].values,
    })

    return parent_df.drop_duplicates().reset_index(drop=True)

def build_dim_academic_support(df):
    """Build academic support dimension with deduplication"""
    def find_col(name):
        for col in df.columns:
            if col.replace('"', '').strip().lower() == name.lower():
                return col
        return None

    academic_df = pd.DataFrame({
        'school_choice_reason': df[find_col('reason')].values,
        'school_support': df[find_col('schoolsup.x')].values,
        'family_support': df[find_col('famsup.x')].values,
        'extra_paid_classes': df[find_col('paid.x')].values,
    })

    return academic_df.drop_duplicates().reset_index(drop=True)

def build_fact_student_performance(df):
    """
    Build performance fact: two rows per student (Math + Portuguese).

    student_id is set directly from the row index (idx + 1), matching the
    explicit student_id written into dim_student. This avoids unreliable
    composite-key lookups that fail when students share demographic attributes.
    """
    def find_col(name):
        for col in df.columns:
            if col.replace('"', '').strip().lower() == name.lower():
                return col
        return None

    # Pre-resolve column names once (not per-row) for performance
    col = {
        'medu': find_col('medu'), 'fedu': find_col('fedu'),
        'mjob': find_col('mjob'), 'fjob': find_col('fjob'),
        'reason': find_col('reason'),
        'schoolsup': find_col('schoolsup.x'), 'famsup': find_col('famsup.x'),
        'paid': find_col('paid.x'),
        'failures_x': find_col('failures.x'), 'absences_x': find_col('absences.x'),
        'studytime_x': find_col('studytime.x'), 'traveltime_x': find_col('traveltime.x'),
        'g1_x': find_col('g1.x'), 'g2_x': find_col('g2.x'), 'g3_x': find_col('g3.x'),
        'failures_y': find_col('failures.y'), 'absences_y': find_col('absences.y'),
        'studytime_y': find_col('studytime.y'), 'traveltime_y': find_col('traveltime.y'),
        'g1_y': find_col('g1.y'), 'g2_y': find_col('g2.y'), 'g3_y': find_col('g3.y'),
    }

    performance_rows = []

    for idx, row in df.iterrows():
        # Shared parent/academic lookup values
        shared = {
            "student_id": idx + 1,   # Direct surrogate — matches dim_student.student_id
            "mother_education_level": row[col['medu']],
            "father_education_level": row[col['fedu']],
            "mother_job_title": row[col['mjob']],
            "father_job_title": row[col['fjob']],
            "school_choice_reason": row[col['reason']],
            "school_support": row[col['schoolsup']],
            "family_support": row[col['famsup']],
            "extra_paid_classes": row[col['paid']],
        }

        # Math record (.x columns)
        math_row = {**shared,
            "subject_name": "Math",
            "prior_class_failures": row[col['failures_x']],
            "total_absences": row[col['absences_x']],
            "weekly_study_time_category": row[col['studytime_x']],
            "commute_time_category": row[col['traveltime_x']],
            "first_period_grade": row[col['g1_x']],
            "second_period_grade": row[col['g2_x']],
            "final_grade": row[col['g3_x']],
        }
        performance_rows.append(math_row)

        # Portuguese record (.y columns)
        port_row = {**shared,
            "subject_name": "Portuguese",
            "prior_class_failures": row[col['failures_y']],
            "total_absences": row[col['absences_y']],
            "weekly_study_time_category": row[col['studytime_y']],
            "commute_time_category": row[col['traveltime_y']],
            "first_period_grade": row[col['g1_y']],
            "second_period_grade": row[col['g2_y']],
            "final_grade": row[col['g3_y']],
        }
        performance_rows.append(port_row)

    performance_df = pd.DataFrame(performance_rows)

    expected_rows = len(df) * 2
    if len(performance_df) != expected_rows:
        raise ValueError(
            f"Grain check failed: expected {expected_rows} performance rows, "
            f"got {len(performance_df)}"
        )

    return performance_df

def build_fact_student_lifestyle(df):
    """
    Build lifestyle fact: one row per student.

    student_id is set directly from the row index (idx + 1), matching the
    explicit student_id written into dim_student.
    """
    def find_col(name):
        for col in df.columns:
            if col.replace('"', '').strip().lower() == name.lower():
                return col
        return None

    lifestyle_df = pd.DataFrame({
        "student_id": range(1, len(df) + 1),   # Direct surrogate key
        "extracurricular_activities": df[find_col("activities.x")].values,
        "attended_nursery_school": df[find_col("nursery")].values,
        "plans_higher_education": df[find_col("higher.x")].values,
        "internet_access": df[find_col("internet")].values,
        "romantic_relationship": df[find_col("romantic.x")].values,
        "family_relationship_quality_score": df[find_col("famrel.x")].values,
        "free_time_index": df[find_col("freetime.x")].values,
        "social_activity_index": df[find_col("goout.x")].values,
        "weekday_alcohol_consumption_level": df[find_col("dalc.x")].values,
        "weekend_alcohol_consumption_level": df[find_col("walc.x")].values,
        "health_status_score": df[find_col("health.x")].values,
    })

    # Do NOT drop_duplicates — grain is one row per student (382 rows required)
    return lifestyle_df.reset_index(drop=True)