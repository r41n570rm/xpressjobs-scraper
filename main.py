import requests
import json
from bs4 import BeautifulSoup
import pandas as pd

# Request headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://xpress.jobs/jobs?KeyWord=cyber&SeoKeyword=cyber-jobs&page=1&pageSize=100',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Priority': 'u=0',
}

# Request parameters
params = {
    'page': '1',
    'pageSize': '1000',
    'keyword': 'software',
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

# Grab links for each job
job_list = []
for job in response:
  job_link = job['jobId']
  job_list.append(f"https://xpress.jobs/api/jobs/publishedJob?jobId={job_link}")