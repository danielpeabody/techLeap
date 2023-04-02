import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import re
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.maximize_window()

# Create an empty DataFrame with column names
df = pd.DataFrame(columns=['Job Title', 'Company', 'Location', 'Job Type', 'Description','Link'])
job_listing = []
main = "https://www.remoterocketship.com/"
page = driver.get(main)

# Get the current window handle
current_window = driver.current_window_handle

#Find button to choose junior
experience = "//input[@id='react-select-⚪️ Experience-input']"
#driver.find_element_by_xpath(experience).click()
driver.find_element("xpath", experience).click()

time.sleep(3)

# Find the div element by its class name (replace "div-class" with the actual class name of the div)
div_element = driver.find_element('id',"react-select-⚪️ Experience-listbox")
#junior = driver.find_element_by_xpath("//div[contains(@class, 'css-qr46ko')]//div[contains(text(), 'Junior')]").click()
junior = driver.find_element("xpath", "//div[contains(@class, 'css-qr46ko')]//div[contains(text(), 'Junior')]").click()
time.sleep(5)
job_elements = driver.find_elements("xpath","//div[@class = 'sm:w-8/12 list-none']")
num_li_tags = len(job_elements)

# Find all the buttons with the class name (buttons to change page)
buttons = driver.find_elements(By.CSS_SELECTOR,".mx-2.py-2.px-3.sm\:px-4.rounded-lg.cursor-pointer.bg-button-secondary")

# Find the maximum integer value of the buttons
max_value = max(int(page_button.text.strip()) for page_button in buttons)

# max_value+1

# Click each button in order
for j in range(1):
    
    #Exceptions are for in case it does not find the job listing or if it could not interact with
    try:
        page_button = driver.find_element("xpath",f"//span[text()='{j+1}']")
        page_button.click()
        time.sleep(3)
    except NoSuchElementException:
        
        #handle the exception by skipping the step
        print("No Such Button Page Element, skipping step...")
    except ElementNotInteractableException:
        # handle the exception by waiting for the element to become interactable
        print("Element Button Page not Interactable, skipping step...")

    for i in range(num_li_tags):
        
        #handle the exception if it could not click on the job_listing
        try:
            xpath = "//div[@class = 'sm:w-8/12 list-none'][{}]".format(i+1)
            job_element = driver.find_element("xpath",xpath)
            job_element.click()
        except NoSuchElementException:
            # handle the exception by skipping the step
            print("Could not click on the Job Listing, skipping step...")
            
        #This will switch the driver to the tab that was opened
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(2)
        
        #Here it will try to get all job title, the location, job type and description if it doesnt find them
        #It will skip the step.
        try:
            #Finding the Title
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            job_title = driver.find_element("xpath","//h1[@class = 'text-3xl font-semibold text-primary']")
            job_title = job_title.text

            
            #Finding the description
            info = driver.find_elements('xpath',"//p[@class = 'text-secondary whitespace-pre-line']")
            info[0].text
            info[1].text
            description = info[0].text + info[1].text

            #Finding the Company Name
            company_name = driver.find_element("xpath","//h2[@class = 'text-lg font-semibold text-center text-primary mb-1 mt-2']")
            company_name = company_name.text
    
            
            # Div and p where the location and job type are located
            job_info = soup.find('div', class_='bg-primary sm:w-10/12 flex flex-col items-start')
            div_span = job_info.find_all('p', class_='text-sm font-semibold text-primary')
            
            #Finding the location
            location = div_span[0].text
            
            #Finding the Job Type
            #Since job type could be in either the 1,2, or 3 element i add them together and later clean
            job_type = div_span[1].text + div_span[2].text + div_span[3].text
            salary = div_span[1].text + div_span[2].text + div_span[3].text
            
        except NoSuchElementException:
            # handle the exception by skipping the step
            print("No Element in the Job Listing, skipping step...")

        try:
            #Finding the Link
            job_link = driver.find_element("xpath","//a[@target = '_blank']")
            job_link.click()
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(3)
            link = driver.current_url
        except TimeoutException:
            print("Timeout exception occurred. closing driver...")
            link = ""
            driver.close()
        except NoSuchElementException:
            print("NoSuchElement exception occurred trying to find the link. closing tab...")
            link = ""
            driver.close()

        
        #Cleaning location
        #Regular expression to remove emojis
        regional_indicator_regex = re.compile("[^a-zA-Z]")
        
        #Removing the emojis by replacing it with ""
        clean_location = regional_indicator_regex.sub("", location)
        
        #Cleaning job_type
        #Remove emojis and text that is not job_listing
        clean_job_type = re.compile(r'(Full Time|Part Time|Contract/Temporary|Internship)')
        job_type_text = clean_job_type.search(job_type)
        
        if job_type_text:
            job_type_text = job_type_text.group()
        else:
            job_type_text = ""
            
        #Cleaning Salary
        clean_s = re.compile(r'(\$[,\d]+(\.\d+)?\s*(k|K|m|M)?\s*-\s*\$[,\d]+(\.\d+)?\s*(k|K|m|M)?\s*\/\s*(year|Year)|\$[,\d]+(\.\d+)?\s*(k|K|m|M)?\s*\/\s*(year|Year)|£[,\d]+(\.\d+)?\s*-\s*£[,\d]+(\.\d+)?\s*\/\s*(year|Year))')
        salary_text = clean_s.search(salary)
        if salary_text:
            salary_text = salary_text.group()
        else:
            salary_text = ""
        #Cleaning Description and adding to dictionary
        cleaned_description = description.replace("•", "")
        def truncate_text(description, max_length=200):
            if len(description) <= max_length:
                return description
            else:
                description = description[:max_length]
                last_space = description.rfind(' ')
            if last_space == -1:
                return description + '...'
            else:
                return description[:last_space] + '...'
            
        job_dict = {
        'job_title': job_title,
        'company': company_name,
        'location': clean_location,
        'job_type': job_type_text,
        'job_snippet': cleaned_description,
        'salary': salary_text,
        'company_rating': "",
        'href': link
                }
        
        # Append dictionary to job_list
        job_listing.append(job_dict)
        
        # Check if there are multiple tabs open
        if len(driver.window_handles) > 1:
        # Loop through the open tabs and close them, except for the current tab
            for window in driver.window_handles:
                if window != current_window:
                    driver.switch_to.window(window)
                    driver.close()
            # Switch back to the original tab
            driver.switch_to.window(current_window)
        
        #new_row
        # Append the new row to the original DataFrame
        #df = df.append(job_dict, ignore_index=True)
        df = pd.DataFrame(job_listing)
        df = df.replace({'company_rating': {'': 'N/A'}})
        df = df.replace({'salary': {'': 'N/A'}})
        #df = df.iloc[::-1]
    string = "We are in Page {}.".format(j+1)
    print(string)
df.to_csv('remoterocketship_final.csv', index = False)