
"""
By: Bruce Noonan
Program: SimplyHired_scraping.py
ISTA 498 Capstone
Purpose: This program uses Selenium to scrape job listings from SimplyHired.com. These jobs are for individuals who have
just graduated from college or have gotten certifications and have little to no job experience. The result of this program
is a csv file that has unique job postings that a new gradute can apply for.
"""

from selenium import webdriver
from time import sleep
from numpy import random
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import numpy as np
import csv 
import os

def scrape_data(lst_of_jobs):
    """
    scrape_data uses Selenium and goes through SimplyHired.com scraping each page for a specific job.
    Args: 
        lst_of_jobs (list) - a list containing a list of tech job titles
    Returns:
        lst (list) - a list of lists containing the html for each page
    """
    lst = []
    service_obj = Service('C:\Program Files (x86)\chromedriver.exe') # the location of the chromedriver on your machine
    user_agent = ('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6)' +
                     'AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8') 
    op = Options() 
    op.add_argument(user_agent)
    op.add_argument("headless")
    for i in lst_of_jobs:
        driver = webdriver.Chrome(options=op, service=service_obj)
        driver.get(f"https://www.simplyhired.com/search?q=entry+level+{i}&l=United+States")
        lst.append(driver.page_source)
        sleeptime = random.uniform(2,10)
        sleep(sleeptime)
        while True:
            try:
                next_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/div/div[3]/div/div/div[1]/div/div[2]/div/nav/a[5]')))
                next_link.click()
                lst.append(driver.page_source)
                sleeptime = random.uniform(2,10)
                sleep(sleeptime)
            except TimeoutException:
                break
        driver.quit()
        sleeptime = random.uniform(2,10)
        sleep(sleeptime)
    return lst

def get_soup(lst):
    """
    get_soup converts the raw html into a BeautifulSoup object
    Args:
        lst (list) - this is a list of lists containing the raw html from the scrape_data function
    Returns:
        a list of lists with all the BeautifulSoup objects
    """
    return [BeautifulSoup(i, 'html.parser') for i in lst]

def find_job_id(lst, id_val='job-list'):
    """
    find_job_id takes the BeautifulSoup objects from the get_soup function and finds the id with
    all the information needed.
    Args:
        lst (list) - this is a list of lists of BeautifulSoup objects
        id_val (string) - this is the id value we want to find with the default value set to 'job-list'
    Returns:
        a list of lists with all all the info in the job id 
    """
    return [i.find(id=id_val) for i in lst]

def get_job_info(soup_job_list, tag, attr=''):
    """
    get_job_info extracts all the info for each job listing
    Args:
        soup_job_list (list) - a list of lists created in the find_job_id function
        tag (string) - this is a string of the tag we want to extract the data from
        attr (dictionary) - this is a dictionary with strings as their key and value, it represents the
        attributes where our data lies (ex. 'data-testid': 'companyName')
    Returns:
        res (list) - this is a list of all the data contained in the tag and attr
    """
    res = []
    for data in soup_job_list:
        if data:
            for li in data.find_all("li"):
                if li.find_all(tag, attrs=attr) == []:
                    res.append('N/A')
                for tag_val in li.find_all(tag, attrs=attr):
                    res.append(tag_val.text)
    return res

def get_job_href(soup_job_list):
    """
    get_job_href extracts the link to the job posting
    Args: 
        soup_job_list (list) - a list of lists created in the find_job_id function
    Returns:
        job_href (list) - this is a list of the hrefs for each job
    """
    job_href = []
    for data in soup_job_list:
        if data:
            for li in data.find_all("li"):
                if li.find_all('a', href=True) == []:
                    job_href.append('N/A')
                for a_tag in li.find_all('a', href=True):
                    job_href.append('simplyhired.com'+a_tag['href'])
    return job_href

def to_df(lst):
    """
    to_df converts all the data into a pandas data frame, removes dupliactes, and any senior level postition.
    Args: 
        lst (list) - this is a list of lists where each element, [titles, company, location, snippet, salary, rating, href],
        contains different data for all the jobs.
    Returns:
        df (DataFrame) - a pandas DataFrame with all the data so it can be easily used for analysis or other purposes.
    """
    df = pd.concat([pd.Series(i) for i in lst], axis = 1)
    df.columns = ['job_title', 'company', 'location', 'job_snippet', 'salary', 'company_rating', 'href']
    df = df.drop_duplicates().reset_index(drop=True)
    mask = df['job_title'].str.contains('Senior|Sr\.|senior|sr\.|sr', case=False)
    df = df[~mask].reset_index(drop=True)
    return df

def to_csv(df, fname):
    """
    to_csv converts the data frame made in the to_df function into a csv file or if the file already exists it
    overwrites that csv
    Args:
        df (DataFrame) - our SimplyHired data frame
        fname (string) - the file we want to create or add to
    """
    df.to_csv(fname, mode='w', index=False, header=True, encoding="utf-8-sig")

    
fname = 'SimplyHired_data.csv'
job_lst = ['software+engineer', 'data+analyst', 'data+scientist', 'network+engineer', 'computer+engineer',
                'security+engineer', 'web+developer', 'computer+systems+analyst', 'cloud+engineer', 
                'database+administrator', 'ui+designer', 'ux+designer', 'mobile+developer', 'full+stack+developer',
                'business+analyst', 'system+engineer', 'system+administrator', 'data+architect',
                'cloud+architect']# comment this list out for testing so it doesnt take forever. Feel free to add more jobs if you'd like.
#job_lst = ['insert job in same format as above'] <- for testing purposes, ui/ux seemed to have the least job postings.
scraped_data = scrape_data(job_lst)
soup = get_soup(scraped_data)
soup_job_list = find_job_id(soup)
titles = get_job_info(soup_job_list, 'a')
company = get_job_info(soup_job_list, 'span', {'data-testid': 'companyName'})
location = get_job_info(soup_job_list, 'span', {'data-testid': 'searchSerpJobLocation'})
snippet = get_job_info(soup_job_list, 'p', {'data-testid': 'searchSerpJobSnippet'})
salary = get_job_info(soup_job_list, 'p', {'data-testid': ['searchSerpJobSalaryEst','searchSerpJobSalaryConfirmed']})
rating = get_job_info(soup_job_list, 'span', {'data-testid': 'searchSerpJobCompanyRating'})
href = get_job_href(soup_job_list)
df = to_df([titles, company, location, snippet, salary, rating, href])
to_csv(df, fname)
