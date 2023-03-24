import requests
from bs4 import BeautifulSoup
import csv

url = 'https://jobs.workable.com/search?location=United%20States%20of%20America&remote=false'

response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

job_listings = soup.find_all('div', class_='job')

with open('job_postings.csv', mode='w', newline='') as csv_file:
    fieldnames = ['title', 'company', 'location', 'summary']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()

    for job in job_listings:
        title = job.find('a', class_='job-title').text.strip()
        company = job.find('span', class_='company-name').text.strip()
        location = job.find('div', class_='location').text.strip()
        summary = job.find('div', class_='description').text.strip()

        writer.writerow({'title': title, 'company': company, 'location': location, 'summary': summary})
print("running")

input("Press Enter to exit...")
