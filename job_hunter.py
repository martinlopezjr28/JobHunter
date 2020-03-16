import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

f_string = '%(asctime)s : %(name)s : %(levelname)s - %(message)s - %(lineno)d'
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
        # requests.get(url)


monster_search = Monster('Python Developer', 'San Jose', 'CA', '95128')
monster_search.results()
