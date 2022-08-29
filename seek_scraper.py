import requests
import csv
from bs4 import BeautifulSoup

# url from Seek based on what to search for (e.g Product Manager/Melbourne/Full Time/Last 24 Hours)
url = 'https://www.seek.com.au/product-manager-jobs/in-All-Melbourne-VIC/full-time?classification=6076%2C6281&daterange=1'

file = open('seek-jobs.csv', 'a')
writer = csv.writer(file)
writer.writerow(['Title', 'Apply'])

def seek_scraper(webpage, page_number):
    # If it's the first page, no need to modify url, every subsequent needs 'next page' spliced in.
    if page_number == 0:
        next_page = webpage
    else: 
        next_page = webpage + '&page=' + str(page_number) + '&sortmode=ListedDate'

    # Setting up Soup to get the html content.
    response = requests.get(next_page)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Running through jobs on each page and collating them.
    jobs = soup.find_all('article', class_='yvsb870')
    for job in jobs:
            job_title = str(job.find('h3', class_='yvsb870').text)

            # Formating Job Link as an actual link. (Should refactor to make a bit cleaner.)
            string = str(job.find('a', class_='yvsb870 yvsb87f h3f08he _14uh9945e _14uh994j _14uh994k _14uh994l _14uh994m'))
            string_set = string.split()
            result = [i for i in string_set if i.startswith('href')]
            interm = ''.join(result)
            job_link = 'https://www.seek.com.au' + interm[5:]
            job_link = job_link.replace('"', "")

            writer.writerow([
                job_title,
                job_link
            ])
    
    print('Seek Jobs Written')

    # Repeat process for three pages (should be enough to cover 24 hours worth of jobs) 
    if page_number < 4:
        page_number = page_number + 1
        seek_scraper(webpage, page_number)
    else:
        file.close()
        print('File done')

seek_scraper(url, 0)


 
