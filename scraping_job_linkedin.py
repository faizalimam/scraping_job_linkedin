import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.parse

#list keywords that used for search job in libnked in
keyword = ['Data Analyst','Business Intelligence Analyst','Marketing Analyst']
# transform keyword into url format
url_keyword = [urllib.parse.quote_plus(key) for key in keyword]

#create csv file for stored data of list jobs that we want to find
file = open('linkedin-jobs.csv', 'a', encoding='utf-8')
writer = csv.writer(file)
writer.writerow(['Title', 'Company', 'Location', 'URL'])

#function for scraping list jobs in linkedin based on keywords that we make
def linkedin_scraper(webpage, page_number):
    next_page = webpage + str(page_number)
    print(str(next_page))

    try:
        response = requests.get(str(next_page))
    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        print("Connection Error")
        return 0
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        print("URL Error")
        raise SystemExit(e)

    soup = BeautifulSoup(response.content,'html.parser')
    jobs = soup.find_all('div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
#     print(soup)
    for job in jobs:
        job_title = job.find('h3', class_='base-search-card__title').text.strip()
        job_company = job.find('h4', class_='base-search-card__subtitle').text.strip()
        job_location = job.find('span', class_='job-search-card__location').text.strip()
        job_link = job.find('a', class_='base-card__full-link')['href']

        writer.writerow([
            job_title,
            job_company,
            job_location,
            job_link
            ]
        )


#main code for scraping
for i in url_keyword:
    page_number = 0
    url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords='+ i +'&location=Indonesia&geoId=102478259&trk=public_jobs_jobs-search-bar_search-submit&start='
    while(page_number < 750):
        linkedin_scraper(url, page_number)
        print('Success add 25 Data - '+ i )
        page_number = page_number + 25

file.close()
print('File closed')

#code for get description jobs
data = pd.read_csv("linkedin-jobs.csv",header=0, encoding='windows-1252')

file2 = open('linkedin-jobs_desc.csv', 'w', encoding='utf-8')
writer2 = csv.writer(file2)
writer2.writerow(['Title', 'Company', 'Location', 'URL','Description'])

for index,row in data.iterrows():
    try:
        response = requests.get(row['URL'])

    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        print("Connection Error")
        jobs=""
        continue
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        print("URL Error")
        jobs=""
        raise SystemExit(e)

    try :
        soup = BeautifulSoup(response.content,'html.parser')
        jobs = soup.find('div', class_='show-more-less-html__markup').get_text(separator=' ')
    except :
        print("no desc")
        jobs=""

    print(row)
    print("desc :"+jobs)
    writer2.writerow([
            row['Title'],
            row['Company'],
            row['Location'],
            row['URL'],
            jobs
            ]
        )
file2.close()
print('File closed')
