import csv

with open('jobs.csv', mode='r', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file)
    row_count = sum(1 for row in reader)
    print(f'Number of rows in the file: {row_count}')

