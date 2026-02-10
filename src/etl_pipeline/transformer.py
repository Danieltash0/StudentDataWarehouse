def transform_data(raw_df):
    df = raw_df.copy()

    # Normalizing the column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    BOOLEAN_COLS = [
        "schoolsup", "famsup", "paid", "activities",
        "nursery", "higher", "internet", "romantic"
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


# Dimensions
def build_dim_student(df):
    cols = ["sex", "age", "address", "guardian", "romantic"]
    return (
        df[cols]
        .drop_duplicates()
        .reset_index(drop=True)
    )


def build_dim_subject(df):
    return (
        df[["subject_name"]]
        .assign(subject_name=lambda x: x["subject_name"].str.strip())
        .drop_duplicates()
        .reset_index(drop=True)
    )


def build_dim_family(df):
    cols = [
        "famsize", "pstatus", "medu", "fedu",
        "mjob", "fjob", "famrel", "famsup"
    ]
    return (
        df[cols]
        .drop_duplicates()
        .reset_index(drop=True)
    )


def build_dim_school(df):
    cols = [
        "school", "reason", "schoolsup", "paid",
        "activities", "nursery", "higher", "internet"
    ]

    return (
        df[cols]
        .rename(columns={"school": "school_code"})
        .drop_duplicates()
        .reset_index(drop=True)
    )

#The fact table is built 
def build_fact_student_performance(
    df, dim_student, dim_family, dim_school, dim_subject
):
    fact = df.merge(
        dim_student.assign(student_id=dim_student.index + 1),
        on=["sex", "age", "address", "guardian", "romantic"],
        how="left"
    )

    fact = fact.merge(
        dim_family.assign(family_id=dim_family.index + 1),
        on=["famsize", "pstatus", "medu", "fedu", "mjob", "fjob", "famrel", "famsup"],
        how="left"
    )

    fact = fact.merge(
        dim_school.assign(school_id=dim_school.index + 1),
        left_on=["school", "reason", "schoolsup", "paid", "activities", "nursery", "higher", "internet"],
        right_on=["school_code", "reason", "schoolsup", "paid", "activities", "nursery", "higher", "internet"],
        how="left"
    )

    fact = fact.merge(
        dim_subject.assign(subject_id=dim_subject.index + 1),
        on="subject_name",
        how="left"
    )

    return fact[[
        "student_id",
        "family_id",
        "school_id",
        "subject_id",
        "traveltime",
        "studytime",
        "failures",
        "freetime",
        "goout",
        "dalc",
        "walc",
        "health",
        "absences",
        "g1",
        "g2",
        "g3"
    ]]

