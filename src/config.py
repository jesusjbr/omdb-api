from datetime import timedelta
from os import environ

# OMDB API
OMDB_API_KEY: str = environ.get("OMDB_API_KEY")
OMDB_API_URL: str = environ.get("OMDB_API_URL", default="https://www.omdbapi.com/")
# DATABASE CONFIGURATION
DATABASE_ENDPOINT: str = environ.get("DATABASE_ENDPOINT")
DATABASE_USER: str = environ.get("DATABASE_USER")
DATABASE_PASSWORD: str = environ.get("DATABASE_PASSWORD")
DATABASE_PORT: str = environ.get("DATABASE_PORT")
DATABASE_NAME: str = environ.get("DATABASE_NAME")
POOL_SIZE: int = int(environ.get("POOL_SIZE", default=5))
POOL_MAX_OVERFLOW: int = int(environ.get("POOL_MAX_OVERFLOW", default=0))
DATABASE_URL: str = "postgresql+asyncpg://{}:{}@{}:{}/{}"
USE_FALLBACK: int = int(environ.get("USE_FALLBACK", default=0))
# TOKEN CONFIGURATION
SECRET_KEY: str = environ.get("SECRET_KEY", default="X1s4GqRfG1lkfhznF0FhIEBqhh2cb8W7gFkzM7z1zjY=")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_TIME_DELTA = timedelta(hours=1)
# USERS FOR DEMO PURPOSES, IN A PRODUCTION APP IMPLEMENT AN ENDPOINT FOR REGISTER INSTEAD
REGULAR_USER_PASSWORD = "1234"
REGULAR_USER_USERNAME = "demo_user"
REGULAR_USER_IS_ADMIN = False
ADMIN_USER_PASSWORD = "12345"
ADMIN_USER_USERNAME = "admin_user"
ADMIN_USER_IS_ADMIN = True


# Constants
TAG_MOVIE: str = "Movies"
TAG_USER: str = "Users"
TYPE_MOVIE: str = "movie"
MAX_TOTAL_RESULTS: int = 100
RESULTS_PER_PAGE: int = 10
MAX_TOTAL_PAGES: int = int(MAX_TOTAL_RESULTS / RESULTS_PER_PAGE)
MOVIES_SEARCH_TERM: str = "Avengers"
ORDER_BY_TITLE = "title"
ORDER_TYPE_ASC = "asc"
ORDER_BY_ID = "id"
AUTHORIZATION_HEADER = "Authorization"
IMDB_ID_UNIQUE_CONSTRAINT = "movie_imdb_id_key"
PROJECT_NAME = "Brite test with OMDB"
API_V1 = "v1"
