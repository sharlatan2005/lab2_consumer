from sqlalchemy.engine import URL

from os import getenv
from dotenv import load_dotenv

load_dotenv()

POSTGRES_CONFIG = URL.create(
    drivername='postgresql+psycopg2',
    username=getenv('PG_DB_USER'),
    password=getenv('PG_DB_PASS'),
    host=getenv('PG_DB_HOST'),
    port=getenv('PG_DB_PORT'),
    database=getenv('PG_DB_NAME')
)

QUEUE_USER = getenv('QUEUE_USER')
QUEUE_PASSWORD = getenv('QUEUE_PASSWORD')
QUEUE_HOST = getenv('QUEUE_HOST')
QUEUE_PORT = getenv('QUEUE_PORT')
QUEUE_NAME = getenv('QUEUE_NAME')

SOCKET_HOST = getenv('SOCKET_HOST')
SOCKET_PORT = int(getenv('SOCKET_PORT'))

TRANSPORT = getenv('TRANSPORT')