import csv
import re
import pandas as pd

def parse_log_line(line):
    """Parse a single line of the log file and return a dictionary with the extracted information."""
    log_pattern = re.compile(
        r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - '
        r'(?P<level>\w+) - '
        r'File: (?P<file>.*?), Path: (?P<path>.*?), Column: (?P<column>.*?), '
        r'Issue: (?P<issue>.*?), Indices: (?P<indices>.*)'
    )
    match = log_pattern.match(line)
    if match:
        return match.groupdict()
    return None

def read_log_file(log_file_path):
    """Read the log file and extract the relevant information."""
    log_entries = []
    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            log_entry = parse_log_line(line)
            if log_entry:
                log_entries.append(log_entry)
    return log_entries

def write_csv_file(log_entries, csv_file_path):
    """Write the extracted log information to a CSV file."""
    keys = log_entries[0].keys() if log_entries else []
    with open(csv_file_path, 'w', newline='') as csv_file:
        dict_writer = csv.DictWriter(csv_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(log_entries)

def main():
    log_file_path = 'data_quality.log'
    csv_file_path = 'data_quality_issues.csv'
    
    log_entries = read_log_file(log_file_path)
    write_csv_file(log_entries, csv_file_path)
    print(f"CSV file created at {csv_file_path}")

if __name__ == "__main__":
    main()
