TITLE & CREDITS:
Project: techLeap

Contributors: Daniel Peabody, Anita Nwude-Chenge, Bruce Noonan,Alexander Esparza, Tolu Adedoja

DESCRIPTION:
techLeap is a job searching web app that is focused on displaying entry level tech jobs to users on the platform.
Our goal with creating techLeap was to design a space where people trying to break into the tech industry can search
and apply for jobs. The site is responsive and will work on all screen sizes. The site perfoms best on firefox, but 
also works on most modern browers including: Chrome, Edge, and Safari. The site is deployed on a digital ocean droplet
at the URL: http://147.182.136.50:3000/  There are four seperate pages on the site that all serve a different function 
for the app. The file structure can be seen below:
-techLeap
    -node_modules
    -public-html
        .about.css
        .about.html
        .contact.css
        contact.html
        index.css
        index.html
        jobs.css
        jobs.html
        script.js
    -package.json
    .READ.md
    .remoterocketship.csv
    .remoterocketship.py
    .server.js
    .SimplyHired_data.csv
    .SimplyHired_scraping.py

--about.css & about.html--
This is the page where users can get an idea of techLeap is all about. It includes our mission 
and some information about who the site is targeted towards. about.css styles about.html which 
holds the contect for the page.

--contact.css & about.html--
This page allows users to submit questions, or feedback. The form directs the message to the 
Daniel Peabodys email who is the project manager of the project. The form submission leverages
the 3rd party system "formsubmit" which ensures the person sending the message is a real person
and not a bot. 

--index.css & index.html--
This is the landing page for our site. Users will not spend much time on this page however
our goal was to create an eyecatching landing page that would encourage users to explore the site.

--jobs.css & jobs.html--
This page contains all of the jobs available on our site at a given time and allows users to search for 
different jobs. This is where users will spend most of the time on the site and this page is connected to 
script.js, a local javascript file. 

--script.js--
This script contains all of the front end logic for the website. No logic was needed for the other three pages
so this script only interacts with jobs.html. This script contains two functions: "jobsearch()" and "shuffle()".
The jobsearch function contains all the logic for searching for a job. The function makes two fetch requests to the 
server and sends parameters based on the inputs from the user to filter the job board. Jobsearch then takes the data
that is sent from the server and converts it to json. For each job the function dynamically creates a dom object with
the data specific to the given job. The dom object is then added to a list. This list is then sent to the shuffle 
function which shuffles the array to make sure job data from both remoterockship.csv and simplyhired_data.csv are 
represented equally. 

--remoterocketship.csv--
Holds the data from remoterocketship.py.

--remoterocketship.py--
This file contains the scraping logic for scraping remoterocketship.com. This file can be downloaded and tested 
by adding it to any folder on the testers computer. This script works by going through each page on the site
and selecting entry level tech positions. After completing the scrape the python file creates a new csv titled
"remoterocketship.py" if that file does not exist or rewrites the existing one. The file includes function 
comments that describe how each function works. 
Dependencies:
pandas
numpy
beautifulsoup
selenium
chromedriver
time
re

--SimplyHired_data.csv--
Holds the data from SimplyHired_data.csv.

--SimplyHired_scraping.py--
This file contains the scraping logic for scraping simplyhired.com. This file can be downloaded and tested 
by adding it to any folder on the testers computer. This script works by  searching the job site for specific tech related jobs 
and then cleans the data by removing senior level postions.  After completing the scrape the python file creates a new 
csv titled "remoterocketship.py" if that file does not exist or rewrites the existing one. The file includes function 
comments that describe how each function works.
Dependencies:
pandas
numpy
beautifulsoup
selenium
chromedriver
time
re

Server.js
This is the server that controls the entire program. The server uses express to route users to the static pages found 
on the site. Upon starting the server the server reads the csv files and stores them in an array to be used later. After 
reading the csv the server than sets an interval to be ran every 3 days to update the local csv files by calling the 
python files that scrape the websites. The sever has two get functions that each get called by the script.js file 
for the needed data to be displayed. Each get function takes the parameters given by the url from the script.js file
and creates a new list of jobs, based on the users search, and sends the requested data back to the client to display.
Dependencies:
Express
csv-parser
fs
child_process
stream

HOW TO USE
We recommend using firefox as it allows for the best performance on the site however any modern browser is supported. 
Jobs are only added to the page after clicking the search button. To search for all jobs on the site simply leave 
all of the inputs blank and click the search button. To narrow the search include different parameters for each 
search box.  

