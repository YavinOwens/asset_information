import pandas as pd
import logging
import os

# Example data
data = {
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'age': [25, 30, None, 22, 28],
    'gender': ['F', 'M', 'M', 'M', 'F'],
    'email': ['alice@example.com', 'bob@example.com', 'charlie@example', 'david@example.com', 'eve@example.com']
}
df = pd.DataFrame(data)

# File details
file_name = 'example_data.csv'
file_path = os.path.abspath(file_name)

# Initialize log reference counter
log_ref_counter = 0

# Data quality check functions
def check_missing_values(df: pd.DataFrame) -> pd.Series:
    """Check for missing values in the DataFrame."""
    logging.debug("Checking for missing values.")
    return df.isnull().sum()

def get_missing_value_indices(df: pd.DataFrame) -> dict:
    """Get indices of missing values for each column."""
    missing_value_indices = {}
    for column in df.columns:
        missing_indices = df[df[column].isnull()].index.tolist()
        if missing_indices:
            missing_value_indices[column] = missing_indices
    return missing_value_indices

def check_duplicates(df: pd.DataFrame) -> int:
    """Check for duplicate rows in the DataFrame."""
    logging.debug("Checking for duplicate rows.")
    return df.duplicated().sum()

def get_duplicate_indices(df: pd.DataFrame) -> list:
    """Get indices of duplicate rows."""
    return df[df.duplicated()].index.tolist()

def check_inconsistencies(df: pd.DataFrame, column: str, valid_values: list) -> pd.Series:
    """Check for inconsistencies in a specific column."""
    logging.debug(f"Checking for inconsistencies in column '{column}'.")
    return df[~df[column].isin(valid_values)][column]

def get_inconsistency_indices(df: pd.DataFrame, column: str, valid_values: list) -> list:
    """Get indices of inconsistent values in a specific column."""
    return df[~df[column].isin(valid_values)].index.tolist()

# Logging configuration
logging.basicConfig(filename='data_quality.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def log_data_quality_issue(level: str, file_name: str, file_path: str, column_name: str, issue: str, indices: list):
    """Log a data quality issue with a reference number."""
    global log_ref_counter
    log_ref_counter += 1
    indices_str = ", ".join(map(str, indices))
    message = f"Ref: {log_ref_counter}, File: {file_name}, Path: {file_path}, Column: {column_name}, Issue: {issue}, Indices: {indices_str}"
    if level == 'DEBUG':
        logging.debug(message)
    elif level == 'INFO':
        logging.info(message)
    elif level == 'WARNING':
        logging.warning(message)
    elif level == 'ERROR':
        logging.error(message)

def report_data_quality_issues(df: pd.DataFrame, file_name: str, file_path: str):
    """Generate a report of data quality issues."""
    logging.info("Starting data quality checks.")
    
    total_records = len(df)
    
    try:
        missing_values = check_missing_values(df)
        missing_value_indices = get_missing_value_indices(df)
        for column, count in missing_values.items():
            if count > 0:
                passed = total_records - count
                indices = missing_value_indices[column]
                log_data_quality_issue('INFO', file_name, file_path, column, f"Missing Values: {count} (Passed: {passed}, Failed: {count})", indices)
            else:
                log_data_quality_issue('INFO', file_name, file_path, column, f"No missing values found. (Passed: {total_records}, Failed: 0)", [])
    except Exception as e:
        log_data_quality_issue('ERROR', file_name, file_path, 'All Columns', f"Error checking missing values: {e}", [])
    
    try:
        duplicates = check_duplicates(df)
        duplicate_indices = get_duplicate_indices(df)
        if duplicates > 0:
            passed = total_records - duplicates
            log_data_quality_issue('INFO', file_name, file_path, 'All Columns', f"Duplicate Rows: {duplicates} (Passed: {passed}, Failed: {duplicates})", duplicate_indices)
        else:
            log_data_quality_issue('INFO', file_name, file_path, 'All Columns', f"No duplicate rows found. (Passed: {total_records}, Failed: 0)", [])
    except Exception as e:
        log_data_quality_issue('ERROR', file_name, file_path, 'All Columns', f"Error checking duplicates: {e}", [])
    
    try:
        gender_inconsistencies = check_inconsistencies(df, 'gender', ['M', 'F'])
        inconsistency_indices = get_inconsistency_indices(df, 'gender', ['M', 'F'])
        if not gender_inconsistencies.empty:
            for inconsistency in gender_inconsistencies.unique():
                count = (gender_inconsistencies == inconsistency).sum()
                passed = total_records - count
                indices = inconsistency_indices
                log_data_quality_issue('WARNING', file_name, file_path, 'gender', f"Inconsistent Value: {inconsistency} (Passed: {passed}, Failed: {count})", indices)
        else:
            log_data_quality_issue('INFO', file_name, file_path, 'gender', f"No gender inconsistencies found. (Passed: {total_records}, Failed: 0)", [])
    except Exception as e:
        log_data_quality_issue('ERROR', file_name, file_path, 'gender', f"Error checking gender inconsistencies: {e}", [])
    
    logging.info("Data quality checks completed.")

# Report data quality issues
report_data_quality_issues(df, file_name, file_path)

print(f"Data quality issues logged in 'data_quality.log'.")
