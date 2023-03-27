import requests
from bs4 import BeautifulSoup
import csv
import os.path
from datetime import datetime
import chardet

url = 'https://jobs.workable.com/search?location=United%20States%20of%20America&remote=false'

response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

job_listings = soup.find_all('div', class_='job')

csv_file_path = 'jobs.csv'

with open(csv_file_path, mode='rb') as csv_file:
    result = chardet.detect(csv_file.read())
    encoding = result['encoding']

with open(csv_file_path, mode='r', encoding=encoding) as csv_file:
    fieldnames = ['title', 'company', 'location', 'summary', 'jobtitle', 'companyrating', 'href', 'jobsnippet', 'salary']
    reader = csv.DictReader(csv_file)
    rows = [row for row in reader]
    row_count = len(rows)

with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()

    for row in rows:
        writer.writerow(row)

    for job in job_listings:
        title = job.find('a', class_='job-title').text.strip()
        company = job.find('span', class_='company-name').text.strip()
        location = job.find('div', class_='location').text.strip()
        summary = job.find('div', class_='description').text.strip()
        jobtitle = job.find('a', class_='job-title')['title']
        companyrating = job.find('span', class_='company-rating').text.strip()
        href = job.find('a', class_='job-title')['href']
        jobsnippet = job.find('div', class_='job-snippet').text.strip()
        salary = job.find('span', class_='salary').text.strip()

        writer.writerow({
            'title': title, 
            'company': company, 
            'location': location, 
            'summary': summary,
            'jobtitle': jobtitle,
            'companyrating': companyrating,
            'href': href,
            'jobsnippet': jobsnippet,
            'salary': salary
        })

    print("running")
    print(f'Number of rows in the file: {row_count}')

print("Last modified time:", datetime.fromtimestamp(os.path.getmtime(csv_file_path)))

input("Press Enter to exit...")
