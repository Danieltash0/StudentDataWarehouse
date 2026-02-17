import pandas as pd
from typing import Optional

SCHOOL_MAP = {
    "GP": "Gabriel Pereira",
    "MS": "Mousinho da Silveira"
}

SEX_MAP = {
    "F": "Female",
    "M": "Male"
}

ADDRESS_MAP = {
    "U": "Urban",
    "R": "Rural"
}

FAMSIZE_MAP = {
    "LE3": "Less or Equal to 3",
    "GT3": "Greater than 3"
}

PSTATUS_MAP = {
    "T": "Living Together",
    "A": "Apart"
}

EDUCATION_MAP = {
    0: "None",
    1: "Primary Education",
    2: "5th to 9th Grade",
    3: "Secondary Education",
    4: "Higher Education"
}

TRAVELTIME_MAP = {
    1: "< 15 Minutes",
    2: "15 to 30 Minutes",
    3: "30 Minutes to 1 Hour",
    4: "> 1 Hour"
}

STUDYTIME_MAP = {
    1: "< 2 Hours",
    2: "2 to 5 Hours",
    3: "5 to 10 Hours",
    4: "> 10 Hours"
}

LIKERT_5_MAP = {
    1: "Very Low / Very Bad",
    2: "Low",
    3: "Moderate",
    4: "High",
    5: "Very High / Excellent"
}

YES_NO_MAP = {
    "yes": "Yes",
    "no": "No"
}

def transform_data(df):
    df["school"] = df["school"].map(SCHOOL_MAP)
    df["sex"] = df["sex"].map(SEX_MAP)
    df["address"] = df["address"].map(ADDRESS_MAP)

    df["famsize_desc"] = df["famsize"].map(FAMSIZE_MAP)
    df["Pstatus_desc"] = df["Pstatus"].map(PSTATUS_MAP)

    for col in ["Medu", "Fedu", "traveltime", "studytime", "famrel", "freetime", "goout", "Dalc", "Walc", "health"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df["Medu_desc"] = df["Medu"].map(EDUCATION_MAP)
    df["Fedu_desc"] = df["Fedu"].map(EDUCATION_MAP)
    df["traveltime_desc"] = df["traveltime"].map(TRAVELTIME_MAP)
    df["studytime_desc"] = df["studytime"].map(STUDYTIME_MAP)
    df["famrel_desc"] = df["famrel"].map(LIKERT_5_MAP)
    df["freetime_desc"] = df["freetime"].map(LIKERT_5_MAP)
    df["goout_desc"] = df["goout"].map(LIKERT_5_MAP)
    df["Dalc_desc"] = df["Dalc"].map(LIKERT_5_MAP)
    df["Walc_desc"] = df["Walc"].map(LIKERT_5_MAP)
    df["health_desc"] = df["health"].map(LIKERT_5_MAP)

    yes_no_cols = [
        "schoolsup", "famsup", "paid",
        "activities", "nursery",
        "higher", "internet", "romantic"
    ]
    for col in yes_no_cols:
        df[col] = df[col].map(YES_NO_MAP)

    region_map = {
        "Gabriel Pereira": "Region 1",
        "Mousinho da Silveira": "Region 2"
    }
    df["region_name"] = df["school"].map(region_map)
    
    if "subject" not in df.columns:
        import numpy as np
        df["subject_name"] = np.random.choice(["Math", "Portuguese"], len(df))
    
    return df

def build_dimensions(df):
    dim_parent_education = (
        df[["Medu", "Fedu"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    dim_parent_job = (
        df[["Mjob", "Fjob"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    dim_location = (
        df[["address"]]
        .drop_duplicates()
        .reset_index(drop=True)
        .rename(columns={"address": "address"})
    )

    dim_guardian = (
        df[["guardian"]]
        .drop_duplicates()
        .reset_index(drop=True)
        .rename(columns={"guardian": "guardian_type"})
    )

    region_map = {
        "Gabriel Pereira": "Region 1",
        "Mousinho da Silveira": "Region 2"
    }
    df["region_name"] = df["school"].map(region_map)
    
    dim_region = (
        df[["region_name"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    region_mapping = {row['region_name']: idx + 1 for idx, row in dim_region.iterrows()}
    df['temp_region_id'] = df['region_name'].map(region_mapping)
    
    dim_school = (
        df[["school", "temp_region_id"]]
        .drop_duplicates()
        .reset_index(drop=True)
        .rename(columns={"temp_region_id": "region_id"})
    )

    if "subject_name" not in df.columns:
        df["subject_name"] = "Math"  # or appropriate subject
    
    dim_subject = (
        df[["subject_name"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    return {
        "dim_parent_education": dim_parent_education,
        "dim_parent_job": dim_parent_job,
        "dim_location": dim_location,
        "dim_guardian": dim_guardian,
        "dim_region": dim_region,
        "dim_school": dim_school,
        "dim_subject": dim_subject,
    }


def build_family_dimension(df: pd.DataFrame, engine) -> pd.DataFrame:
    dim_parent_education = pd.read_sql(
        "SELECT parent_edu_id, Medu, Fedu FROM dim_parent_education", engine
    )
    dim_parent_job = pd.read_sql(
        "SELECT parent_job_id, Mjob, Fjob FROM dim_parent_job", engine
    )

    edu_map = dim_parent_education.set_index(["Medu", "Fedu"])["parent_edu_id"].to_dict()
    job_map = dim_parent_job.set_index(["Mjob", "Fjob"])["parent_job_id"].to_dict()

    tmp = df[["famsize", "Pstatus", "famrel", "Medu", "Fedu", "Mjob", "Fjob"]].copy()
    tmp["parent_edu_id"] = tmp.apply(lambda r: edu_map.get((r["Medu"], r["Fedu"])), axis=1)
    tmp["parent_job_id"] = tmp.apply(lambda r: job_map.get((r["Mjob"], r["Fjob"])), axis=1)

    tmp["famrel"] = pd.to_numeric(tmp["famrel"], errors="coerce").astype("Int64")
    tmp["parent_edu_id"] = pd.to_numeric(tmp["parent_edu_id"], errors="coerce").astype("Int64")
    tmp["parent_job_id"] = pd.to_numeric(tmp["parent_job_id"], errors="coerce").astype("Int64")

    dim_family = (
        tmp[["famsize", "Pstatus", "famrel", "parent_edu_id", "parent_job_id"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    return dim_family


def build_student_dimension(df: pd.DataFrame, engine) -> pd.DataFrame:
    dim_location = pd.read_sql("SELECT location_id, address FROM dim_location", engine)
    dim_guardian = pd.read_sql("SELECT guardian_id, guardian_type FROM dim_guardian", engine)

    loc_map = dim_location.set_index("address")["location_id"].to_dict()
    guard_map = dim_guardian.set_index("guardian_type")["guardian_id"].to_dict()

    tmp = df[["sex", "age", "internet", "higher", "romantic", "address", "guardian"]].copy()
    tmp["location_id"] = tmp["address"].map(loc_map)
    tmp["guardian_id"] = tmp["guardian"].map(guard_map)

    tmp["age"] = pd.to_numeric(tmp["age"], errors="coerce").astype("Int64")
    tmp["location_id"] = pd.to_numeric(tmp["location_id"], errors="coerce").astype("Int64")
    tmp["guardian_id"] = pd.to_numeric(tmp["guardian_id"], errors="coerce").astype("Int64")

    dim_student = (
        tmp[
            [
                "sex",
                "age",
                "internet",
                "higher",
                "romantic",
                "location_id",
                "guardian_id",
            ]
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    return dim_student

def build_fact_table(df, engine):
    print("Building fact table...")
    
    print("Loading dimensions from database...")
    dim_subject = pd.read_sql("SELECT subject_id, subject_name FROM dim_subject", engine)
    dim_school = pd.read_sql("SELECT school_id, school, region_id FROM dim_school", engine)
    dim_location = pd.read_sql("SELECT location_id, address FROM dim_location", engine)
    dim_guardian = pd.read_sql("SELECT guardian_id, guardian_type FROM dim_guardian", engine)
    dim_parent_education = pd.read_sql("SELECT parent_edu_id, Medu, Fedu FROM dim_parent_education", engine)
    dim_parent_job = pd.read_sql("SELECT parent_job_id, Mjob, Fjob FROM dim_parent_job", engine)
    dim_family = pd.read_sql("SELECT * FROM dim_family", engine)
    dim_student = pd.read_sql("SELECT * FROM dim_student", engine)
    dim_region = pd.read_sql("SELECT region_id, region_name FROM dim_region", engine)
    
    #print(f"Loaded {len(dim_guardian)} guardian records")
    #print(f"Loaded {len(dim_school)} school records")
    #print(f"Loaded {len(dim_region)} region records")

    needed_cols = ['school', 'address', 'guardian', 'sex', 'age', 'internet', 'higher', 
                   'romantic', 'famsize', 'Pstatus', 'famrel', 'Medu', 'Fedu', 'Mjob', 'Fjob',
                   'traveltime', 'studytime', 'failures', 'freetime', 'goout', 'Dalc', 'Walc', 
                   'health', 'absences', 'G1', 'G2', 'G3']
    
    if 'subject' in df.columns:
        df['subject_name'] = df['subject']
        needed_cols.append('subject_name')
    elif 'subject_name' in df.columns:
        needed_cols.append('subject_name')
    else:
        df['subject_name'] = 'Math'
        needed_cols.append('subject_name')
    
    fact_df = df[needed_cols].copy()
    #print(f"Working with {len(fact_df)} rows")

    def _dedupe_for_index(dim_df: pd.DataFrame, key_col: str, id_col: Optional[str], dim_name: str) -> pd.DataFrame:
        """
        Ensure key_col is unique so Series.map() won't raise InvalidIndexError.
        Keeps the lowest id_col when provided, otherwise keeps the first occurrence.
        """
        if key_col not in dim_df.columns:
            return dim_df

        if dim_df[key_col].isna().any():
            dim_df = dim_df.dropna(subset=[key_col])

        if dim_df[key_col].duplicated().any():
            before = len(dim_df)
            if id_col and id_col in dim_df.columns:
                dim_df = dim_df.sort_values(id_col, kind="mergesort")
            dim_df = dim_df.drop_duplicates(subset=[key_col], keep="first")
        return dim_df

    dim_subject = _dedupe_for_index(dim_subject, "subject_name", "subject_id", "dim_subject").set_index("subject_name")
    dim_location = _dedupe_for_index(dim_location, "address", "location_id", "dim_location").set_index("address")
    dim_guardian = _dedupe_for_index(dim_guardian, "guardian_type", "guardian_id", "dim_guardian").set_index("guardian_type")
    dim_school = _dedupe_for_index(dim_school, "school", "school_id", "dim_school").set_index("school")

    #print("Performing dimension lookups...")
    
    fact_df['subject_id'] = fact_df['subject_name'].map(dim_subject['subject_id'])
    
    fact_df['location_id'] = fact_df['address'].map(dim_location['location_id'])
    fact_df["location_id"] = pd.to_numeric(fact_df["location_id"], errors="coerce").astype("Int64")
    
    fact_df['guardian_id'] = fact_df['guardian'].map(dim_guardian['guardian_id'])
    fact_df["guardian_id"] = pd.to_numeric(fact_df["guardian_id"], errors="coerce").astype("Int64")
    
    fact_df['school_id'] = fact_df['school'].map(dim_school['school_id'])
    
    dim_parent_education = dim_parent_education.set_index(['Medu', 'Fedu'])
    edu_mapping = dim_parent_education['parent_edu_id'].to_dict()
    fact_df['parent_edu_id'] = fact_df.apply(
        lambda row: edu_mapping.get((row['Medu'], row['Fedu'])), axis=1
    )
    fact_df["parent_edu_id"] = pd.to_numeric(fact_df["parent_edu_id"], errors="coerce").astype("Int64")
    
    dim_parent_job = dim_parent_job.set_index(['Mjob', 'Fjob'])
    job_mapping = dim_parent_job['parent_job_id'].to_dict()
    fact_df['parent_job_id'] = fact_df.apply(
        lambda row: job_mapping.get((row['Mjob'], row['Fjob'])), axis=1
    )
    fact_df["parent_job_id"] = pd.to_numeric(fact_df["parent_job_id"], errors="coerce").astype("Int64")

    
    family_merge_cols = ['famsize', 'Pstatus', 'famrel', 'parent_edu_id', 'parent_job_id']

    if "famrel" in fact_df.columns:
        fact_df["famrel"] = pd.to_numeric(fact_df["famrel"], errors="coerce").astype("Int64")
    for col in ["famrel", "parent_edu_id", "parent_job_id"]:
        if col in dim_family.columns:
            dim_family[col] = pd.to_numeric(dim_family[col], errors="coerce").astype("Int64")
    
    fact_df = fact_df.merge(
        dim_family[['family_id'] + family_merge_cols],
        on=family_merge_cols,
        how='left'
    )
    
    student_merge_cols = ['sex', 'age', 'internet', 'higher', 'romantic', 'location_id', 'guardian_id']

    for col in ["age", "location_id", "guardian_id"]:
        if col in dim_student.columns:
            dim_student[col] = pd.to_numeric(dim_student[col], errors="coerce").astype("Int64")
    
    fact_df = fact_df.merge(
        dim_student[['student_id'] + student_merge_cols],
        on=student_merge_cols,
        how='left',
        suffixes=('', '_student')
    )
    
    fact_columns = [
        'student_id', 'family_id', 'school_id', 'subject_id',
        'traveltime', 'studytime', 'failures', 'freetime',
        'goout', 'Dalc', 'Walc', 'health', 'absences',
        'G1', 'G2', 'G3'
    ]
    
    available_cols = [col for col in fact_columns if col in fact_df.columns]
    
    fact_table = fact_df[available_cols].copy()
    
    key_cols = ['student_id', 'family_id', 'school_id', 'subject_id']
    existing_key_cols = [col for col in key_cols if col in fact_table.columns]
    
    before_drop = len(fact_table)
    fact_table = fact_table.dropna(subset=existing_key_cols)
    after_drop = len(fact_table)
    
    #print(f"Dropped {before_drop - after_drop} rows with missing foreign keys")
    print(f"Fact table built with {len(fact_table)} rows")
    
    for col in existing_key_cols:
        fact_table[col] = fact_table[col].astype(int)
    
    return fact_table