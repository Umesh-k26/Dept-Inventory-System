from fastapi import Depends, FastAPI, HTTPException, status
from fastapi import Body, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from functools import wraps
from pydantic import BaseModel
from typing import Annotated
from auth import get_email
from configs import Config
from pypika import Query, Table, Tuple, Parameter, Criterion

from db.connect import conn

from models.db import User, Asset, Bulk_Asset, Order_Table
from models.responses import AssetDetails

import datetime

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get-role/")
async def get_test(email: Annotated[str ,Depends(get_email)]):
    # print(f"email is {email}")
    # print(Config.GOOGLE_CLIENT_ID)
    return {"role": "admin"}

# USER details

@app.post("/add-user")
async def add_user(user : User, email: Annotated[str, Depends(get_email)]):
  try:
    q = Query.into('users').insert(user.user_id, user.first_name, user.last_name, user.gmail, user.user_type, user.department)
    with conn.cursor() as cur:
       cur.execute(q.get_sql())
    conn.commit()
  except Exception as e:
     print(e)
     conn.rollback()
     raise HTTPException(400, "Cant add user")
  return {"message": "user added"}
  

@app.delete("/delete-user/{user_id}")
async def delete_user(user_id: str, email: Annotated[str, Depends(get_email)]):
  try:
    users = Table('users')
    q = Query.from_(users).delete().where(users.user_id.ilike(f'{user_id}'))
    with conn.cursor() as cur:
        cur.execute(q.get_sql())
    conn.commit()
  except Exception as e:
    print(e)
    raise HTTPException(201, "User not found")
  return {"message" : "user deleted"}

@app.post("/update-user/")
async def update_user(user : User, email: Annotated[str, Depends(get_email)]) -> User:
  try:
    users = Table('users')
    q = Query.update(users).where(users.user_id == user.user_id)
    q1 = Query.from_(users).select(users.star).where(users.user_id == user.user_id)
    set_list = {}
    if user.user_type:
      set_list['user_type'] = user.user_type
    if user.gmail:
      set_list[users.gmail] = user.gmail
    if user.department:
      set_list[users.department] = user.department
    if user.first_name:
      set_list[users.first_name] = user.first_name
    if user.last_name:
      set_list[users.last_name] = user.last_name
    for k in set_list.keys():
      q = q.set(k, set_list[k])
    with conn.cursor() as cur:
       cur.execute(q.get_sql())
       cur.execute(q1.get_sql())
       result = cur.fetchall()
    conn.commit()
  except Exception as e:
     print(e)
     conn.rollback()
     raise HTTPException(400, "Cant update user")
  return User.parse_obj(result[0])


@app.get("/get-user/{user_id}")
def get_user(user_id : str) -> User:
  try:
    users = Table('users')
    q = Query.from_(users).select(users.star).where(users.user_id == user_id)
    with conn.cursor() as cur:
        cur.execute(q.get_sql())
        user = cur.fetchall()
  except Exception as e:
    print(e)
    raise HTTPException(201, "User not found")
  return User.parse_obj(user[0])


@app.get("/get-user")
def filter_user(user : Annotated[User, Query()]) -> list[User]:
  try:
    users = Table('users')
    q = Query.from_(users).select(users.star)
    criterion_list = []
    if user.user_id:
      criterion_list.append(users.user_id.ilike(f'%{user.user_id}%'))
    if user.user_type:
      criterion_list.append(users.user_type.ilike(f'{user.user_type}'))
    if user.gmail:
      criterion_list.append(users.gmail == user.gmail)
    if user.department:
      criterion_list.append(users.department.ilike(f'%{user.department}%'))
    if user.first_name:
      criterion_list.append(users.first_name.ilike(f'%{user.first_name}%'))
    if user.last_name:
      criterion_list.append(users.last_name.ilike(f'%{user.last_name}%'))
    q = q.where(
      Criterion.all(criterion_list)
    )
    with conn.cursor() as cur:
        cur.execute(q.get_sql())
        results = cur.fetchall()
  except Exception as e:
    print(e)
    raise HTTPException(201, "filters not found")
  return [User.parse_obj(user_) for user_ in results]

#ASSET details

@app.post("/add-asset")
async def add_asset(asset : Asset):
  try:
    q = Query.into('asset').insert(asset.asset_name, asset.serial_no, asset.model, asset.department, asset.asset_location, asset.asset_holder, asset.entry_date, asset.unit_price, asset.warranty, asset.is_hardware, asset.system_no, asset.purchase_order_no, asset.asset_state, asset.picture)
    with conn.cursor() as cur:
       cur.execute(q.get_sql())
    conn.commit()
  except Exception as e:
     print(e)
     conn.rollback()
     raise HTTPException(400, "Cant add asset")
  return {"message" : "asset added"}
  

@app.delete("/delete-asset/{serial_no}")
async def delete_asset(serial_no : str):
  try:
    asset = Table('asset')
    q = Query.from_(asset).delete().where(asset.serial_no.ilike(f'{serial_no}'))
    with conn.cursor() as cur:
        cur.execute(q.get_sql())
    conn.commit()
  except Exception as e:
    print(e)
    raise HTTPException(201, "Asset not found")
  return {'message' : "asset deleted"}


@app.post("/update-asset/")
async def update_asset(asset_ : Asset) -> Asset:
  # picture ka data type check karna hai
  try:
    asset = Table('asset')
    q = Query.update(asset).where(asset.serial_no == asset_.serial_no)
    q1 = Query.from_(asset).select(asset.star).where(asset.serial_no == asset_.serial_no)
    set_list = {}
    if asset_.asset_name:
      set_list['asset_name'] = asset_.asset_name
    if asset_.model:
      set_list['model'] = asset_.model
    if asset_.department:
      set_list['department'] = asset_.department
    if asset_.asset_location:
      set_list['asset_location'] = asset_.asset_location
    if asset_.entry_date:
      set_list['entry_date'] = asset_.entry_date
    if asset_.unit_price:
      set_list['unit_price'] = asset_.unit_price
    if asset_.warranty:
      set_list['warranty'] = asset_.warranty
    if asset_.is_hardware:
      set_list['is_hardware'] = asset_.is_hardware
    if asset_.system_no:
      set_list['system_no'] = asset_.system_no
    if asset_.purchase_order_no:
      set_list['purchase_order_no'] = asset_.purchase_order_no
    if asset_.asset_state:
      set_list['asset_state'] = asset_.asset_state
    if asset_.picture:
      set_list['picture'] = asset_.picture
    for k in set_list.keys():
      q = q.set(k, set_list[k])
    with conn.cursor() as cur:
       cur.execute(q.get_sql())
       cur.execute(q1.get_sql())
       result = cur.fetchall()
    conn.commit()
  except Exception as e:
     print(e)
     conn.rollback()
     raise HTTPException(400, "Cant add asset")
  return Asset.parse_obj(result)



#ORDER details

@app.post("/add-order")
async def add_order(order : Order_Table):
  try:
    q = Query.into('order_table').insert(order.purchase_order_no, order.order_date, order.indentor, order.firm_name, order.financial_year, order.gst_tin, order.final_procurement_date, order.invoice_no, order.invoice_date)
    with conn.cursor() as cur:
       cur.execute(q.get_sql())
    conn.commit()
  except Exception as e:
     print(e)
     conn.rollback()
     raise HTTPException(400, "Cant add order")
  return {"message" : "order added"}
  

@app.post("/delete-order/{purchase_order_no}{invoice_no}")
async def delete_asset(purchase_order_no : str, invoice_no : str):
  try:
    order = Table('order_table')
    q = Query.from_(order).delete().where(order.purchase_order_no.ilike(f'%{purchase_order_no}%') & order.invoice_no.ilike(f'%{invoice_no}%'))
    with conn.cursor() as cur:
        cur.execute(q.get_sql())
    conn.commit()
  except Exception as e:
    print(e)
    raise HTTPException(201, "Order not found")
  return {"message" : "order deleted"}


@app.post("/update-order/")
async def add_order(order_ : Order_Table) -> Order_Table:
  try:
    order = Table('order_table')
    q = Query.update(order).where(order.purchase_order_no.ilike(f'%{order_.purchase_order_no}%') & order.invoice_no.ilike(f'%{order_.invoice_no}%'))
    q1 = Query.from_(order).select(order.star).where(order.purchase_order_no.ilike(f'%{order_.purchase_order_no}%') & order.invoice_no.ilike(f'%{order_.invoice_no}%'))
    set_list = {}
    if order_.order_date:
      set_list['order_date'] = order_.order_date
    if order_.indentor:
      set_list['indentor'] = order_.indentor
    if order_.firm_name:
      set_list['firm_name'] = order_.firm_name
    if order_.financial_year:
      set_list['financial_year'] = order_.financial_year
    if order_.gst_tin:
      set_list['gst_tin'] = order_.gst_tin
    if order_.final_procurement_date:
      set_list['final_procurement_date'] = order_.final_procurement_date
    if order_.invoice_date:
      set_list['invoice_date'] = order_.invoice_date
    for k in set_list.keys():
      q = q.set(k, set_list[k])
    with conn.cursor() as cur:
       cur.execute(q.get_sql())
       cur.execute(q.get_sql())
       result = cur.fetchall()
    conn.commit()
  except Exception as e:
     print(e)
     conn.rollback()
     raise HTTPException(400, "Cant update order")
  return Order_Table.parse_obj(result)
