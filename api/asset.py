from fastapi import Depends, HTTPException, UploadFile, File, Body
from typing import Annotated
from configs import Config
from pypika import Query, Table, Criterion
from psycopg2 import Binary

from db.connect import conn

from models.db import Asset, Bulk_Asset
from models.responses import AssetDetails

import datetime
from fastapi import APIRouter


router_asset = APIRouter()

origins = [
    "http://localhost:3000",
]

#ASSET details

@router_asset.post("/add-asset")
async def add_asset(asset_: Annotated[Asset, Body()], picture: UploadFile = File(...)):
  try:
    pic = await picture.read()
    # pic = base64.b64encode(pic)
    print(type(pic))
    print(asset_)
    q = Query.into('asset').insert(asset_.asset_name, asset_.model, asset_.serial_no, asset_.department, asset_.asset_location, asset_.asset_holder, asset_.entry_date, asset_.unit_price, asset_.warranty, asset_.is_hardware, asset_.system_no, asset_.purchase_order_no, asset_.asset_state,Binary(pic))
    with conn.cursor() as cur:
       cur.execute(q.get_sql())
    conn.commit()
  except Exception as e:
     print(e)
     conn.rollback()
     raise HTTPException(400, "Cant add asset")
  return {"message" : "asset added"}
  

@router_asset.delete("/delete-asset/{serial_no}")
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


@router_asset.put("/update-asset/")
async def update_asset(asset_ : Asset):
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
    print(result)
  except Exception as e:
     print(e)
     conn.rollback()
     raise HTTPException(400, "Cant update asset")
  return Asset.parse_obj(result[0])


@router_asset.post("/get-asset")
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
    order_list = set([i['purchase_order_no'] for i in asset_details])
    user_list = set([i['asset_holder'] for i in asset_details])
    q1 = Query.from_(order).select(order.star).where(
      Criterion.any( order.purchase_order_no == i for i in order_list)
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
