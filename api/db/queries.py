import aiosql
import pathlib

from db.built_queries import(
    add_asset,
    get_asset,
    add_bulk_asset,
    get_bulk_asset 
)

queries = aiosql.aiosql

queries.add_asset = add_asset
queries.get_asset = get_asset
queries.add__bulk_asset = add_bulk_asset
queries.get_bulk_asset = get_bulk_asset

