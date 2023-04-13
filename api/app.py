from fastapi import Depends, FastAPI, HTTPException, status
from fastapi import Body, Form, Query, Request
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
    q = Query.into('users').insert(user.user_id, user.first_name, user.last_name, user.email, user.user_type, user.department)
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
    q = Query.update(users).where(users.user_id.ilike(f'{user_id}')).set(users.user_state, 'Unactive')
    with conn.cursor() as cur:
        cur.execute(q.get_sql())
    conn.commit()
  except Exception as e:
    print(e)
    raise HTTPException(201, "User not found")
  return {"message" : "user deleted"}

@app.put("/update-user/")
async def update_user(user : User, email: Annotated[str, Depends(get_email)]) -> User:
  try:
    users = Table('users')
    q = Query.update(users).where(users.user_id == user.user_id)
    q1 = Query.from_(users).select(users.star).where(users.user_id == user.user_id)
    set_list = {}
    if user.user_type:
      set_list[users.user_type] = user.user_type
    if user.email:
      set_list[users.email] = user.email
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


@app.post("/get-user")
def filter_user(user : Annotated[Asset, Query()]) -> list[User]:
  try:
    users = Table('users')
    q = Query.from_(users).select(users.star)
    criterion_list = []
    if user.user_id:
      criterion_list.append(users.user_id.ilike(f'%{user.user_id}%'))
    if user.user_type:
      criterion_list.append(users.user_type.ilike(f'{user.user_type}'))
    if user.email:
      criterion_list.append(users.email == user.email)
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

    q = Query.into('asset').insert(asset.asset_name, asset.model, asset.serial_no, asset.department, asset.asset_location, asset.asset_holder, asset.entry_date, asset.unit_price, asset.warranty, asset.is_hardware, asset.system_no, asset.purchase_order_no, asset.asset_state, asset.picture)
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


@app.put("/update-asset/")
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
  return Asset.parse_obj(result[0])


@app.post("/get-asset")
def filter_asset(asset_ : Asset) -> list[AssetDetails]:
  try:
    user = Table('users')
    asset = Table('asset')
    order = Table('order_table')
    
    criterion_list = []
    if asset_.serial_no:
      criterion_list.append(asset.serial_no.ilike(f'%{asset_.serial_no}%'))
    if asset_.asset_name:
      criterion_list.append(asset.asset_name.ilike(f'%{asset_.asset_name}%'))
    if asset_.model:
      criterion_list.append(asset.model.ilike(f'%{asset_.model}%'))
    if asset_.department:
      criterion_list.append(asset.department.ilike(f'%{asset_.department}%'))
    if asset_.asset_location:
      criterion_list.append(asset.asset_location.ilike(f'%{asset_.asset_location}%'))
    if asset_.asset_holder:
      criterion_list.append(asset.asset_holder.ilike(f'%{asset_.asset_holder}%'))
    if asset_.entry_date:
      criterion_list.append(asset.entry_date.ilike(f'%{asset_.entry_date}%'))
    if asset_.unit_price:
      criterion_list.append(asset.unit_price.ilike(f'%{asset_.unit_price}%'))
    if asset_.warranty:
      criterion_list.append(asset.warranty.ilike(f'%{asset_.warranty}%'))
    if asset_.is_hardware:
      criterion_list.append(asset.is_hardware == asset_.is_hardware)
    if asset_.system_no:
      criterion_list.append(asset.system_no.ilike(f'%{asset_.system_no}%'))
    if asset_.purchase_order_no:
      criterion_list.append(asset.purchase_order_no.ilike(f'%{asset_.purchase_order_no}%'))
    if asset_.asset_state:
      criterion_list.append(asset.asset_state.ilike(f'%{asset_.asset_state}%'))
    
    q = Query.from_(asset).select(asset.star).where(
      Criterion.all(criterion_list)
    )
    with conn.cursor() as cur:
        cur.execute(q.get_sql())
        asset_details = cur.fetchall()
    asset_list = set([i['purchase_order_no'] for i in asset_details])
    user_list = set([i['asset_holder'] for i in asset_details])
    q1 = Query.from_(asset).select(asset.star).where(
      Criterion.any( asset.purchase_order_no == i for i in asset_list)
      )
    q2 = Query.from_(user).select(user.user_id, user.first_name, user.last_name).where(
      Criterion.any( user.user_id == i for i in user_list)
      )
    with conn.cursor() as cur:
        cur.execute(q1.get_sql())
        order_details = cur.fetchall()
        cur.execute(q2.get_sql())
        user_details = cur.fetchall()
    for i in asset_details:
      for j in order_details:
        if i['purchase_order_no'] == j['purchase_order_no']:
          i.update(j)
      for j in user_details:
        if i['asset_holder'] == j['user_id']:
          i.update(j)
  except Exception as e:
    print(e)
    raise HTTPException(201, "filters not found")

  return [AssetDetails.parse_obj(asset) for asset in asset_details]


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
  

@app.delete("/delete-order/{purchase_order_no}{invoice_no}")
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


@app.put("/update-order/")
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

@app.post("/get-order/")
async def get_order(order_ : Order_Table):
  try:
    order = Table('order_table')
    user = Table('users')
    asset = Table('asset')
    criterion_list = []
    if order_.purchase_order_no:
      criterion_list.append(asset.purchase_order_no.ilike(f'%{order_.purchase_order_no}%'))
    if order_.order_date:
      criterion_list.append(asset.order_date.ilike(f'%{order_.order_date}%'))
    if order_.indentor:
      criterion_list.append(asset.indentor.ilike(f'%{order_.indentor}%'))
    if order_.firm_name:
      criterion_list.append(asset.firm_name.ilike(f'%{order_.firm_name}%'))
    if order_.financial_year:
      criterion_list.append(asset.financial_year.ilike(f'%{order_.financial_year}%'))
    if order_.gst_tin:
      criterion_list.append(asset.gst_tin.ilike(f'%{order_.gst_tin}%'))
    if order_.final_procurement_date:
      criterion_list.append(asset.final_procurement_date.ilike(f'%{order_.final_procurement_date}%'))
    if order_.invoice_no:
      criterion_list.append(asset.invoice_no.ilike(f'%{order_.invoice_no}%'))
    if order_.invoice_date:
      criterion_list.append(asset.invoice_date.ilike(f'%{order_.invoice_date}%'))
    q = Query.from_(order).select(order.star).where(
      Criterion.all(criterion_list)
      )
    with conn.cursor() as cur:
        cur.execute(q.get_sql())
        order_details = cur.fetchall()
    asset_list = set([i['purchase_order_no'] for i in order_details])
    user_list = set([i['indentor'] for i in order_details])
    q1 = Query.from_(order).select(order.star).where(
      Criterion.any( order.purchase_order_no == i for i in asset_list)
      )
    q2 = Query.from_(user).select(user.user_id, user.first_name, user.last_name).where(
      Criterion.any( user.user_id == i for i in user_list)
      )
    with conn.cursor() as cur:
        cur.execute(q1.get_sql())
        order_details = cur.fetchall()
        cur.execute(q2.get_sql())
        user_details = cur.fetchall()
    for i in order_details:
      for j in order_details:
        if i['purchase_order_no'] == j['purchase_order_no']:
          i.update(j)
      for j in user_details:
        if i['asset_holder'] == j['user_id']:
          i.update(j)
    conn.commit()
  except Exception as e:
    print(e)
    raise HTTPException(201, "Order not found")
  return "order deleted"