import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

f_string = '%(asctime)s : %(name)s : %(levelname)s - %(message)s'
log_format = logging.Formatter(f_string)

file_handler = logging.FileHandler('log/job_hunter.log')
file_handler.setFormatter(log_format)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_format)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

class Monster():

    def __init__(self, job_name, city, state, zip_code):
        self.job_name = '-'.join(job_name.split(' '))
        self.city = '-'.join(city.split(' '))
        self.state = state
        self.zip_code = zip_code

        logger.debug(f'Job Name: {self.job_name}')

    def results(self):
        url = 'https://www.monster.com/jobs/search/'+\
              f'?q={self.job_name}'+\
              f'&where={self.city}-{self.state}-{self.zip_code}'
        logger.debug(f'URL: {url}')

        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        job_results = soup.find(id='ResultsContainer')

        return job_results

    def scrape_jobs(self, jobs, filter=None):
        jobs_dict = {}
        for job in jobs:
            title = job.find('h2', class_='title')
            company = job.find('div', class_='company')
            location = job.find('div', class_='location')

            if None in (title, company, location):
                continue

            link = job.find('a')['href']
            title_key = title.text.strip()
            company_stripped = company.text.strip()
            location_stripped = location.text.strip()

            jobs_dict[title_key] = {'company': company_stripped,
                                    'location': location_stripped,
                                    'link' : link}
            logger.debug(f'{title_key}: {jobs_dict[title_key]}\n')

    def all_jobs(self):

        job_results = self.results()
        all_jobs = job_results.find_all('section', class_='card-content')
        all_jobs_dict = self.scrape_jobs(all_jobs)

        return all_jobs_dict

    def string_dec(self, filter_key):
        def string_handler(text):
            if text == None:
                return False
            else:
                return filter_key in text.lower()
        return string_handler


    def specific_jobs(self, filter_key) :

        filter_key = filter_key.lower()
        job_results = self.results()
        job_titles = job_results.find_all('h2',
                                    string=self.string_dec(filter_key))
        id_list = [job.find_parent("section")['data-jobid'] for job in job_titles]
        filtered_jobs = job_results.find_all('section',
                                            class_='card-content',
                                            attrs={"data-jobid": lambda text: text in id_list}
                                            )
        filtered_jobs_dict = self.scrape_jobs(filtered_jobs)
        return filtered_jobs_dict


monster_search = Monster('Software Developer', 'San Jose', 'CA', '95128')
monster_search.all_jobs()
monster_search.specific_jobs('python')

