import time
import sqlalchemy
from .extractor import extract_raw_data
from .transformer import (
    transform_data,
    build_dim_student,
    build_dim_subject,
    build_dim_parent_details,
    build_dim_academic_support,
    build_fact_student_performance,
    build_fact_student_lifestyle
)
from .loader import (
    load_table,
    load_fact_student_performance,
    load_fact_student_lifestyle,
    clear_all_tables,
    get_table_counts,
    engine
)

def wait_for_db(retries: int = 15, delay: int = 5) -> None:
    """
    Block until MySQL is accepting connections.
    Even after the Docker healthcheck passes, the server may need a moment.
    """
    for attempt in range(1, retries + 1):
        try:
            with engine.connect():
                print("  Database connection established.")
                return
        except Exception as exc:
            print(f"  Waiting for database... (attempt {attempt}/{retries}) — {exc}")
            time.sleep(delay)
    raise RuntimeError("Could not connect to the database after multiple retries.")


def run_pipeline():
    try:
        print("=" * 50)
        print("STARTING ETL PIPELINE")
        print("=" * 50)
        
        # ── 0. Wait for MySQL ──────────────────────────────
        print("\n0. WAITING FOR DATABASE...")
        wait_for_db()
        
        # Step 1: Extract and transform
        print("\n1. EXTRACTING DATA...")
        raw_df = extract_raw_data()
        print(f"Extracted {len(raw_df)} rows from merged dataset")
        
        print("\n2. TRANSFORMING DATA...")
        clean_df = transform_data(raw_df)
        print(f"Transformed {len(clean_df)} rows")
        
        # Step 2: Build dimensions
        print("\n3. BUILDING DIMENSIONS...")
        dim_student = build_dim_student(clean_df)
        dim_subject = build_dim_subject(clean_df)
        dim_parent_details = build_dim_parent_details(clean_df)
        dim_academic_support = build_dim_academic_support(clean_df)
        
        print(f"Built dim_student: {len(dim_student)} rows")
        print(f"Built dim_subject: {len(dim_subject)} rows")
        print(f"Built dim_parent_details: {len(dim_parent_details)} rows")
        print(f"Built dim_academic_support: {len(dim_academic_support)} rows")
        
        # Check if fallback was used (minimal student dimension)
        if len(dim_student) < len(clean_df) * 0.5:
            print("WARNING: Using fallback student dimension due to data quality issues")
            print("Only loading performance and lifestyle facts for valid students")
            
            # Build facts only for valid students
            valid_student_indices = dim_student['student_id'].tolist()
            valid_clean_df = clean_df[clean_df['student_id'].isin(valid_student_indices)]
            
            fact_performance = build_fact_student_performance(valid_clean_df)
            fact_lifestyle = build_fact_student_lifestyle(valid_clean_df)
        else:
            # Normal flow - build facts for all students
            fact_performance = build_fact_student_performance(clean_df)
            fact_lifestyle = build_fact_student_lifestyle(clean_df)
        
        print(f"Built fact_student_performance: {len(fact_performance)} rows")
        print(f"Built fact_student_lifestyle: {len(fact_lifestyle)} rows")
        
        # Step 4: Validate grain
        print("\n5. VALIDATING DATA GRAIN...")
        expected_performance_rows = len(clean_df) * 2  # 2 subjects per student
        if len(fact_performance) != expected_performance_rows:
            raise ValueError(
                f"Grain validation failed: Expected {expected_performance_rows} performance rows, "
                f"got {len(fact_performance)}"
            )
        
        if len(fact_lifestyle) != len(clean_df):
            raise ValueError(
                f"Grain validation failed: Expected {len(clean_df)} lifestyle rows, "
                f"got {len(fact_lifestyle)}"
            )
        
        print(" Grain validation passed")
        
        # Step 5: Clear existing data
        print("\n6. CLEARING EXISTING DATA...")
        clear_all_tables()
        
        # Step 6: Load dimensions in correct order
        print("\n7. LOADING DIMENSIONS...")
        load_table(dim_student, "dim_student")
        load_table(dim_subject, "dim_subject")
        load_table(dim_parent_details, "dim_parent_details")
        load_table(dim_academic_support, "dim_academic_support")
        
        # Step 7: Load facts in correct order
        print("\n8. LOADING FACTS...")
        load_fact_student_lifestyle(fact_lifestyle)
        load_fact_student_performance(fact_performance)
        
        # Step 8: Verify final counts
        print("\n9. VERIFYING FINAL ROW COUNTS...")
        final_counts = get_table_counts()
        
        print("\nFINAL ROW COUNTS:")
        print("-" * 30)
        for table, count in final_counts.items():
            print(f"{table}: {count}")
        
        # Step 9: Validate expected counts
        print("\n10. VALIDATING EXPECTED COUNTS...")
        expected_counts = {
            "dim_student": len(dim_student),
            "dim_subject": len(dim_subject),
            "dim_parent_details": len(dim_parent_details),
            "dim_academic_support": len(dim_academic_support),
            "fact_student_lifestyle": len(fact_lifestyle),
            "fact_student_performance": len(fact_performance)
        }
        
        validation_passed = True
        for table, expected in expected_counts.items():
            actual = final_counts.get(table)
            if actual != expected:
                print(f" {table}: Expected {expected}, got {actual}")
                validation_passed = False
            else:
                print(f" {table}: {actual} rows")
        
        if validation_passed:
            print("\n" + "=" * 50)
            print("ETL PIPELINE COMPLETED SUCCESSFULLY!")
            print("=" * 50)
            print(f" Processed {len(clean_df)} students")
            print(f" Generated {len(fact_performance)} performance records")
            print(f" Generated {len(fact_lifestyle)} lifestyle records")
        else:
            print("\n" + "=" * 50)
            print("ETL PIPELINE COMPLETED WITH VALIDATION ERRORS!")
            print("=" * 50)
            raise ValueError("Row count validation failed")
            
    except Exception as e:
        print(f"\n ETL PIPELINE FAILED: {str(e)}")
        print("=" * 50)
        raise

if __name__ == "__main__":
    run_pipeline()
