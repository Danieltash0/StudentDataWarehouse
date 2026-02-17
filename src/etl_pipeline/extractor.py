import pandas as pd

def extract_data():
    df_mat = pd.read_csv("data/raw/student-mat.csv", sep=",")
    df_por = pd.read_csv("data/raw/student-por.csv", sep=",")

    #print("MAT COLUMNS:", df_mat.columns.tolist())
    #print("POR COLUMNS:", df_por.columns.tolist())

    df_mat["subject_name"] = "Math"
    df_por["subject_name"] = "Portuguese"
    df = pd.concat([df_mat, df_por], ignore_index=True)
    return df