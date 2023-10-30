import csv

def csv_to_string(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        # Joining each row and column with appropriate formatting
        csv_str = '\n'.join([', '.join(row) for row in csv_reader])
    return csv_str