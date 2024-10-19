import requests
import json
from bs4 import BeautifulSoup
import pandas as pd

# Request headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0'
}

# Get search term from user
job_search_term = input("\nEnter job search term: ")

# Get output filename from user
output_filename = input("Enter output filename (.csv): ")

# Request parameters
params = {
    'page': '1',
    'pageSize': '10000',
    'keyword': job_search_term,
    'locations': '',
    'sectors': '',
    'jobTypes': '',
    'careerLevels': '',
    'sortBy': 'SortedCreateDate DESC',
    'byCVLess': 'false',
    'byWalkIn': 'false',
}

# Get job search results as json
response = requests.get('https://xpress.jobs/api/jobs/searchJobs', params=params, headers=headers).json()

master_list = []

while True:
    print(f"\nSearching for jobs using the keyword \"{job_search_term}\"")
    
    # Grab links for each job
    job_list = []
    print("\nGetting job listing links...")
    for job in response:
        job_link = job['jobId']
        job_list.append(f"https://xpress.jobs/api/jobs/publishedJob?jobId={job_link}")

    # Get job listing information
    print("\nGetting job listing information...")
    for link in job_list:
        data_dict = {}

        job_page = requests.get(link, headers=headers).json() 

        data_dict['Link'] = link                                                      # Job link
        data_dict['Job Title'] = job_page['jobItem']['jobTitle']                      # Job title
        data_dict['Organization Name'] = job_page['jobItem']['organizationName']      # Organization Name
        data_dict['Job Type'] = job_page['jobItem']['jobType']                        # Job type
        data_dict['Locations'] = job_page['jobItem']['locations']                     # Job locations
        data_dict['Overview'] = job_page['jobItem']['overview']                       # Job overview

        job_info_soup = BeautifulSoup(job_page['jobInfo'], 'html.parser')             # Job description 
        data_dict['JobInfo'] = job_info_soup.text                                     

        data_dict['Education'] = job_page['education']                                # Educational requirements
        data_dict['Experience'] =  job_page['experience']                             # Experience requirements
        data_dict['Min. Salary'] = job_page['minSalary']                              # Minimum salary
        data_dict['Max. Salary'] = job_page['maxSalary']                              # Maximum salary
        data_dict['Salary Range'] = job_page['salaryRange']                           # Salary range

        master_list.append(data_dict)
    break


print(f"\nSuccessfully scraped data from {len(job_list)} jobs!\n")    

df = pd.DataFrame(master_list)

df.to_csv(output_filename, index=False)   # Convert pandas dataframe to .csv 