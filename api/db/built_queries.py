from pypika import Query, Table, Tables, Tuple, Parameter, Database
from pypika import functions as fn
from pypika import Criterion as cr
# from pypika import PseudoColumn


def add_asset(conn, body):
    asset = Table("asset")
    q = (Query.into(asset).columns(*body.keys()).insert(*body.values()))
    with conn.cursor() as cur:
        cur.execute(q.get_sql())
    return

def get_asset(conn, body):
    asset, order = Table('asset', 'order_table')
    schema = Database('invertory')
    q1 = Query.from_(schema.COLUMNS).select(schema.COLUMNS.COLUMN_NAME).where(schema.COLUMNS.TABLE_NAME == asset)
    q2 = Query.from_(schema.COLUMNS).select(schema.COLUMNS.COLUMN_NAME).where(schema.COLUMNS.TABLE_NAME == order) 
    
    with conn.cursor() as cur:
        cur.execute(q1.get_sql())
        r1 = cur.fetchall()
        cur.execute(q2.get_sql())
        r2 = cur.fetchall()
    
    asset_key = []
    asset_val = []
    order_key = []
    order_val = []

    for i in body.keys():
        if(i in r1):
            asset_key.append(i)
            asset_val.append(body[i])
        if(i in r2):
            order_key.append(i)
            order_val.append(body[i])

    # col_asset = PseudoColumn(asset_key)
    # col_order = PseudoColumn(order_key)

    q = Query.from_(asset).select(asset.star).where(asset.serial_no == serial_no)
    with conn.cursor() as cur:
        cur.execute(q.get_sql())
        results = cur.fetchall()
    return results

def add_bulk_asset(conn, body):
    bulk_asset = Table("bulk_asset")
    q = (Query.into(bulk_asset).columns(*body.keys()).insert(*body.values()))
    with conn.cursor() as cur:
        cur.execute(q.get_sql())
    return

def get_bulk_asset(conn, user_id : str):
    bulk_asset = Table('bulk_asset')
    q = Query.from_(bulk_asset).select(bulk_asset.star).where(bulk_asset.user_id == user_id)
    with conn.cursor() as cur:
        cur.execute(q.get_sql())
        results = cur.fetchall()
    return results


