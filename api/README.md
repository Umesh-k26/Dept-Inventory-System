## Backend Setup

- Install poetry from [Poetry Install](https://python-poetry.org/docs/#installation)
- Run `cd $ROOT_DIR/api`
- Run `poetry install`

After running the above commands,

## Database Setup (for development)

- Install postgresql from [Postgresql Install](https://www.postgresql.org/download/)
- Run `psql -U postgres` to enter into psql shell
- Run `\i $ROOT_DIR/api/db/schema.sql` to setup the database

## Running the backend

- To initialize poetry environment, run `poetry shell`
- To run the app, run `python3 main.py`

## Running the tests

- Run `export PYTHONPATH=$ROOT_DIR/api:PYTHONPATH`
- Run `python3 $ROOT_DIR/api/tests/test_main.py`
