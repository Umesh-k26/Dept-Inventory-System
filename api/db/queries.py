import aiosql
import pathlib

queries = aiosql.from_path(
    pathlib.Path(__file__).parent / "./simple_queries.sql",
    "psycopg2"
)
