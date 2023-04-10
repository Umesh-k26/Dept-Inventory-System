import psycopg2
from psycopg2.extras import RealDictCursor
from configs import Config

conn = psycopg2.connect(
    dbname = Config.POSTGRES_NAME,
    user = Config.POSTGRES_USER,
    password = Config.POSTGRES_PASS,
    cursor_factory = RealDictCursor,
    host = Config.POSTGRES_HOST
)