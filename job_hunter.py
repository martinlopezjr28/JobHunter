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

    def __init__(self, job_name, location):
        self.job_name = '-'.join(job_name.split(' '))
        self.location = location

        logger.debug(f'Job Name: {self.job_name}')

    def results():
        requests.get('https://www.monster.com/jobs/\
                      search/?q=Software-Developer&where=Australia')
        pass

monster_search = Monster('Python Developer', 'Santa Clara')
