# API Key to include when consuming the OMDB API
from os import environ

OMDB_API_KEY: str = environ.get('OMDB_API_KEY', default='OMDB_API_KEY_NOT_SET')
OMDB_API_URL: str = environ.get('OMDB_API_URL', default='http://www.omdbapi.com/')

# Constants
TAG_MOVIE = "Movies"
TYPE_MOVIE = "movie"
MAX_TOTAL_RESULTS = 100
RESULTS_PER_PAGE = 10
MAX_TOTAL_PAGES = MAX_TOTAL_RESULTS / RESULTS_PER_PAGE