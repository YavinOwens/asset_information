# Data Quality Logging and CSV Conversion Scripts

## Overview

This repository contains two Python scripts: one for logging data quality issues and another for converting the log file into a CSV file. These scripts help ensure data quality by identifying and logging issues such as missing values, duplicate rows, and inconsistent data entries. The logged data is then extracted and formatted into a CSV file for easier analysis.

## Notable Functions

### Data Quality Logging Script (`data_quality_logging.py`)

- **check_missing_values(df: pd.DataFrame) -> pd.Series**: 
  Checks for missing values in the DataFrame and returns the count of missing values per column.
- **get_missing_value_indices(df: pd.DataFrame) -> dict**: 
  Returns the indices of missing values for each column.
- **check_duplicates(df: pd.DataFrame) -> int**: 
  Checks for duplicate rows in the DataFrame and returns the count of duplicate rows.
- **get_duplicate_indices(df: pd.DataFrame) -> list**: 
  Returns the indices of duplicate rows.
- **check_inconsistencies(df: pd.DataFrame, column: str, valid_values: list) -> pd.Series**: 
  Checks for inconsistencies in a specific column based on valid values and returns the inconsistent values.
- **get_inconsistency_indices(df: pd.DataFrame, column: str, valid_values: list) -> list**: 
  Returns the indices of inconsistent values in a specific column.
- **log_data_quality_issue(level: str, file_name: str, file_path: str, column_name: str, issue: str, indices: list)**: 
  Logs a data quality issue with a reference number, including details such as the file name, file path, column name, specific issue, and indices of the records.
- **report_data_quality_issues(df: pd.DataFrame, file_name: str, file_path: str)**: 
  Runs all data quality checks and logs any identified issues.

### Log to CSV Conversion Script (`log_to_csv.py`)

- **parse_log_line(line: str) -> dict**: 
  Parses a single line of the log file and extracts the relevant information into a dictionary.
- **read_log_file(log_file_path: str) -> list**: 
  Reads the log file and extracts the relevant information from each line into a list of dictionaries.
- **write_csv_file(log_entries: list, csv_file_path: str)**: 
  Writes the extracted log information to a CSV file.

## Script Descriptions

### Data Quality Logging Script (`data_quality_logging.py`)

This script performs data quality checks on a DataFrame and logs any identified issues. The checks include:
- Missing values
- Duplicate rows
- Inconsistent data entries

Each issue is logged with a unique reference number, and the log includes details such as the file name, file path, column name, specific issue, and indices of the records with issues.

#### Outputs
- **data_quality.log**: A log file containing detailed information about any data quality issues found during the checks.

### Log to CSV Conversion Script (`log_to_csv.py`)

This script reads the `data_quality.log` file and extracts the logged information into a CSV file. It parses each log entry to retrieve details such as the reference number, timestamp, log level, file name, file path, column name, specific issue, and indices of the records with issues.

#### Outputs
- **data_quality_issues.csv**: A CSV file containing the extracted log information, formatted for easier analysis.

## Example Usage

### Run the Data Quality Logging Script

Save the script as `data_quality_logging.py` and run it:

```sh
python data_quality_logging.py
