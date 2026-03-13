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

    # Check for critical null values first
    critical_fields = ['medu', 'fedu', 'mjob', 'fjob', 'reason']
    null_students = []
    valid_students = []
    
    for idx, row in df.iterrows():
        has_nulls = any(pd.isna(row[find_col(field)]) for field in critical_fields)
        
        if has_nulls:
            null_students.append(idx)
            print(f"Warning: Student {idx} has null values in critical fields: {[field for field in critical_fields if pd.isna(row[find_col(field)])]}")
        
        # Always include student in valid list (with nulls flagged for quality monitoring)
        valid_students.append(idx)
    
    if len(null_students) > 0:
        null_percentage = (len(null_students) / len(df)) * 100
        print(f"Warning: {len(null_students)} students ({null_percentage:.1f}%) have null values in critical fields")
    
    # Use all students for dimension building (including those with nulls)
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

    # Build DataFrame with all students (including those with nulls for monitoring)
    student_df = pd.DataFrame({
        'school': df[cols_map['school']].astype(str),
        'sex': df[cols_map['sex']].astype(str),
        'age': df[cols_map['age']].astype(str),
        'address': df[cols_map['address']].astype(str),
        'family_size': df[cols_map['family_size']].astype(str),
        'parent_cohabitation_status': df[cols_map['parent_cohabitation_status']].astype(str),
        'guardian': df[cols_map['guardian']].astype(str),
    })
    
    # Add explicit 1-based surrogate key so fact tables can reference it directly
    student_df.insert(0, 'student_id', range(1, len(student_df) + 1))

    # Do NOT drop duplicates — each row IS a distinct student (382 rows required)
    # print(f"Built student dimension: {len(student_df)} rows ({len(null_students)} with nulls)")
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
        'mother_education_level': df[find_col('medu')].astype(str),
        'father_education_level': df[find_col('fedu')].astype(str),
        'mother_job_title': df[find_col('mjob')].astype(str),
        'father_job_title': df[find_col('fjob')].astype(str),
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
        'school_choice_reason': df[find_col('reason')].astype(str),
        'school_support': df[find_col('schoolsup.x')].astype(str),
        'family_support': df[find_col('famsup.x')].astype(str),
        'extra_paid_classes': df[find_col('paid.x')].astype(str),
    })

    return academic_df.drop_duplicates().reset_index(drop=True)

def build_fact_student_performance(df):
    """
    Build performance fact: two rows per student (Math + Portuguese).

    student_id is set directly from row index (idx + 1), matching the
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
    null_values_count = {}
    critical_null_count = 0

    for idx, row in df.iterrows():
        # Only check for nulls in CRITICAL fields (parent/academic info)
        # NOT in grade fields - those are expected to have values
        critical_fields = ['medu', 'fedu', 'mjob', 'fjob', 'reason']
        null_fields = []
        
        for field_name in critical_fields:
            if pd.isna(row[col[field_name]]):
                null_fields.append(field_name)
        
        if null_fields:
            null_values_count[idx] = null_fields
            critical_null_count += 1
            print(f"Warning: Student {idx} has null values in critical fields: {null_fields}")
            # Still process the student - just flag the issue
            # We'll use default values for missing critical fields
        
        # Shared parent/academic lookup values with null handling
        shared = {
            "student_id": idx + 1,   # Direct surrogate — matches dim_student.student_id
            "mother_education_level": row[col['medu']] if not pd.isna(row[col['medu']]) else 'Unknown',
            "father_education_level": row[col['fedu']] if not pd.isna(row[col['fedu']]) else 'Unknown',
            "mother_job_title": row[col['mjob']] if not pd.isna(row[col['mjob']]) else 'Unknown',
            "father_job_title": row[col['fjob']] if not pd.isna(row[col['fjob']]) else 'Unknown',
            "school_choice_reason": row[col['reason']] if not pd.isna(row[col['reason']]) else 'Unknown',
            "school_support": row[col['schoolsup']] if not pd.isna(row[col['schoolsup']]) else False,
            "family_support": row[col['famsup']] if not pd.isna(row[col['famsup']]) else False,
            "extra_paid_classes": row[col['paid']] if not pd.isna(row[col['paid']]) else False,
        }

        # Math record (.x columns) - handle null grades with defaults
        math_row = {**shared,
            "subject_name": "Math",
            "prior_class_failures": row[col['failures_x']] if not pd.isna(row[col['failures_x']]) else 0,
            "total_absences": row[col['absences_x']] if not pd.isna(row[col['absences_x']]) else 0,
            "weekly_study_time_category": row[col['studytime_x']] if not pd.isna(row[col['studytime_x']]) else 1,
            "commute_time_category": row[col['traveltime_x']] if not pd.isna(row[col['traveltime_x']]) else 1,
            "first_period_grade": row[col['g1_x']] if not pd.isna(row[col['g1_x']]) else 0,
            "second_period_grade": row[col['g2_x']] if not pd.isna(row[col['g2_x']]) else 0,
            "final_grade": row[col['g3_x']] if not pd.isna(row[col['g3_x']]) else 0,
        }
        performance_rows.append(math_row)

        # Portuguese record (.y columns) - handle null grades with defaults
        port_row = {**shared,
            "subject_name": "Portuguese",
            "prior_class_failures": row[col['failures_y']] if not pd.isna(row[col['failures_y']]) else 0,
            "total_absences": row[col['absences_y']] if not pd.isna(row[col['absences_y']]) else 0,
            "weekly_study_time_category": row[col['studytime_y']] if not pd.isna(row[col['studytime_y']]) else 1,
            "commute_time_category": row[col['traveltime_y']] if not pd.isna(row[col['traveltime_y']]) else 1,
            "first_period_grade": row[col['g1_y']] if not pd.isna(row[col['g1_y']]) else 0,
            "second_period_grade": row[col['g2_y']] if not pd.isna(row[col['g2_y']]) else 0,
            "final_grade": row[col['g3_y']] if not pd.isna(row[col['g3_y']]) else 0,
        }
        performance_rows.append(port_row)

    if critical_null_count > 0:
        print(f"Processed {critical_null_count} students with critical nulls (used default values)")

    performance_df = pd.DataFrame(performance_rows)

    expected_rows = len(df) * 2
    actual_rows = len(performance_df)
    if actual_rows != expected_rows:
        raise ValueError(
            f"Grain check failed: expected {expected_rows} performance rows, "
            f"got {actual_rows} (processed {critical_null_count} with defaults)"
        )

    return performance_df

def build_fact_student_lifestyle(df):
    """
    Build lifestyle fact: one row per student.

    student_id is set directly from row index (idx + 1), matching the
    explicit student_id written into dim_student.
    """
    def find_col(name):
        for col in df.columns:
            if col.replace('"', '').strip().lower() == name.lower():
                return col
        return None

    null_values_count = {}
    critical_null_count = 0
    
    # Process all students, using defaults for null values
    lifestyle_rows = []
    
    for idx, row in df.iterrows():
        # Check for null values in critical fields
        critical_fields = ['activities.x', 'nursery', 'higher.x', 'internet', 'romantic.x']
        null_fields = []
        
        for field_name in critical_fields:
            col_name = find_col(field_name)
            if col_name and pd.isna(row[col_name]):
                null_fields.append(field_name)
        
        if null_fields:
            null_values_count[idx] = null_fields
            critical_null_count += 1
            print(f"Warning: Student {idx} has null values in lifestyle fields: {null_fields}")
        
        # Build lifestyle record with null handling
        lifestyle_row = {
            "student_id": idx + 1,   # Direct surrogate key
            "extracurricular_activities": row[find_col("activities.x")] if not pd.isna(row[find_col("activities.x")]) else False,
            "attended_nursery_school": row[find_col("nursery")] if not pd.isna(row[find_col("nursery")]) else False,
            "plans_higher_education": row[find_col("higher.x")] if not pd.isna(row[find_col("higher.x")]) else False,
            "internet_access": row[find_col("internet")] if not pd.isna(row[find_col("internet")]) else False,
            "romantic_relationship": row[find_col("romantic.x")] if not pd.isna(row[find_col("romantic.x")]) else False,
            "family_relationship_quality_score": row[find_col("famrel.x")] if not pd.isna(row[find_col("famrel.x")]) else 3,
            "free_time_index": row[find_col("freetime.x")] if not pd.isna(row[find_col("freetime.x")]) else 3,
            "social_activity_index": row[find_col("goout.x")] if not pd.isna(row[find_col("goout.x")]) else 3,
            "weekday_alcohol_consumption_level": row[find_col("dalc.x")] if not pd.isna(row[find_col("dalc.x")]) else 1,
            "weekend_alcohol_consumption_level": row[find_col("walc.x")] if not pd.isna(row[find_col("walc.x")]) else 1,
            "health_status_score": row[find_col("health.x")] if not pd.isna(row[find_col("health.x")]) else 3,
        }
        lifestyle_rows.append(lifestyle_row)
    
    if critical_null_count > 0:
        print(f"Processed {critical_null_count} students with lifestyle nulls (used default values)")

    lifestyle_df = pd.DataFrame(lifestyle_rows)

    # Do NOT drop duplicates — grain is one row per student
    return lifestyle_df.reset_index(drop=True)