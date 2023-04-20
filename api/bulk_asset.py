from fastapi import Depends, HTTPException, UploadFile, File, Body, Request
from typing import Annotated
from configs import Config
from pypika import PostgreSQLQuery as Query, Table, Criterion
from psycopg2 import Binary

from db.connect import conn

from models.db import Bulk_Asset
from models.responses import AssetDetails

import datetime
from fastapi import APIRouter

from fastapi_mail import FastMail, MessageSchema, MessageType

from models.email import email, conf 

router_bulk_asset = APIRouter()

origins = [
    "http://localhost:3000",
]

#BULK ASSET details

@router_bulk_asset.post("/add-bulk-asset")
async def add_bulk_asset(req : Request):
  formData = await req.form()

  asset = dict()
  for key in formData.keys():
    if formData.get(key) == '':
      asset[key] = None
    else:
      asset[key] = formData.get(key)
  
  if asset['picture'] is not None:
    pic = await asset['picture'].read()
    pic = Binary(pic)
  else:
    pic = None

  try:
    asset_ = Table('bulk_asset')
    q = Query.into('asset').insert(asset['asset_name'], asset['model'], asset['asset_make'], asset['serial_no'], asset['department'], asset['asset_location'], asset['asset_type'], asset['entry_date'], asset['quantity'], asset['purchase_order_no'], asset['financial_year'], asset['asset_state'], pic)
    q1 = Query.from_(asset_).select(asset_.star).where(asset_.serial_no == asset['serial_no'])
    with conn.cursor() as cur:
       cur.execute(q.get_sql())
    conn.commit()

    with conn.cursor() as cur:
       cur.execute(q1.get_sql())
       result = cur.fetchall()

    result_str = ''
    for i in result[0]:
      if i != 'picture':
        result_str += i + " : " + str(result[0][i]) + "<br>"

    message = MessageSchema(
        subject="Asset Added",
        recipients=email.dict().get("email"),
        body="Dear Admin,<br> The asset with the following details has been added. <br>" + result_str,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    
  except Exception as e:
     print(e)
     conn.rollback()
     raise HTTPException(e)
  return {"message" : "asset added"}
  

@router_bulk_asset.delete("/delete-bulk-asset/{serial_no}")
async def delete_bulk_asset(serial_no : str):
  try:
    asset = Table('bulk_asset')
    q1 = Query.from_(asset).select(asset.serial_no, asset.asset_name, asset.model, asset.asset_location).where(asset.serial_no == serial_no)
    q = Query.from_(asset).delete().where(asset.serial_no.ilike(f'{serial_no}'))
    with conn.cursor() as cur:
        cur.execute(q1.get_sql()) 
        result = cur.fetchall()
        cur.execute(q.get_sql())
    conn.commit()

    result_str = ''
    for i in result[0]:
      if i != 'picture':
        result_str += i + " : " + str(result[0][i]) + "<br>"

    message = MessageSchema(
        subject="Asset Deleted",
        recipients=email.dict().get("email"),
        body="Dear Admin,<br> The asset with the following details has been deleted. <br>" + result_str,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)

  except Exception as e:
    print(e)
    raise HTTPException(201, "Asset not found")
  return {'message' : "asset deleted"}


@router_bulk_asset.put("/update-bulk-asset/")
async def update_bulk_asset(req : Request):
  formData = await req.form()

  asset_ = dict()
  for key in formData.keys():
    if formData.get(key) == '':
      asset_[key] = None
    else:
      asset_[key] = formData.get(key)
  
  if asset_['picture'] is not None:
    pic = await asset_['picture'].read()
    pic = Binary(pic)
  else:
    pic = None

  try:
    asset = Table('asset')
    q = Query.update(asset).where(asset.serial_no == asset_['serial_no'])
    q1 = Query.from_(asset).select(asset.star).where(asset.serial_no == asset_['serial_no'])
    
    set_list = {}
    if asset_['asset_name']:
      set_list['asset_name'] = asset_['asset_name']
    if asset_['model']:
      set_list['model'] = asset_['model']
    if asset_['asset_make']:
      set_list['asset_make'] = asset_['asset_make']
    if asset_['serial_no']:
      set_list['serial_no'] = asset_['serial_no']
    if asset_['department']:
      set_list['department'] = asset_['department']
    if asset_['asset_location']:
      set_list['asset_location'] = asset_['asset_location']
    if asset_['asset_type']:
      set_list['asset_type'] = asset_['asset_type']
    if asset_['entry_date']:
      set_list['entry_date'] = asset_['entry_date']
    if asset_['quantity']:
      set_list['quantity'] = asset_['quantity']
    if asset_['purchase_order_no']:
      set_list['purchase_order_no'] = asset_['purchase_order_no']
    if asset_['financial_year']:
      set_list['financial_year'] = asset_['financial_year']
    if asset_['asset_state']:
      set_list['asset_state'] = asset_['asset_state']
    if pic != None:
      set_list['picture'] = pic
    for k in set_list.keys():
      q = q.set(k, set_list[k])
    with conn.cursor() as cur:
       cur.execute(q.get_sql())
       cur.execute(q1.get_sql())
       result = cur.fetchall()
    conn.commit()

    result_str = ''
    for i in result[0]:
      if i != 'picture' or i != 'barcode':
        result_str += i + " : " + str(result[0][i]) + "<br>"

    message = MessageSchema(
        subject="Asset Updated",
        recipients=email.dict().get("email"),
        body="Dear Admin,<br> The asset with the following details has been updated. <br>" + result_str,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)

    print(result)
  except Exception as e:
     print(e)
     conn.rollback()
     raise HTTPException(400, "Cant update asset")
  return {"message" : "Asset Updated"}


@router_bulk_asset.post("/get-bulk-asset")
def filter_asset(asset_ : Bulk_Asset) -> list[AssetDetails]:
  try:
    asset = Table('bulk_asset')
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
    if asset_.entry_date:
      criterion_list.append(asset.entry_date.ilike(f'%{asset_.entry_date}%'))
    if asset_.quantity:
      criterion_list.append(asset.quantity.ilike(f'{asset_.quantity}'))
    if asset_.purchase_order_no:
      criterion_list.append(asset.purchase_order_no.ilike(f'%{asset_.purchase_order_no}%'))
    if asset_.financial_year:
      criterion_list.append(asset.financial_year.ilike(f'{asset_.financial_year}'))
    if asset_.asset_state:
      criterion_list.append(asset.asset_state.ilike(f'%{asset_.asset_state}%'))
    
    q = Query.from_(asset).select(asset.star).where(
      Criterion.all(criterion_list)
    )
    with conn.cursor() as cur:
        cur.execute(q.get_sql())
        asset_details = cur.fetchall()
    order_list = set([i['purchase_order_no'] for i in asset_details])
    q1 = Query.from_(order).select(order.star).where(
      Criterion.any( order.purchase_order_no == i for i in order_list)
      )
    with conn.cursor() as cur:
        cur.execute(q1.get_sql())
        order_details = cur.fetchall()
    for i in asset_details:
      for j in order_details:
        if i['purchase_order_no'] == j['purchase_order_no']:
          i.update(j)
  except Exception as e:
    print(e)
    raise HTTPException(201, "filters not found")

  return [AssetDetails.parse_obj(asset) for asset in asset_details]

@router_bulk_asset.get("/get-all-bulk-asset")
async def get_all_bulk_asset():
  asset = Table("bulk_asset")
  q = Query.from_(asset).select(asset.serial_no, asset.asset_name, asset.model, asset.asset_make, asset.department, asset.asset_location, asset.asset_type, asset.entry_date, asset.quantity, asset.purchase_order_no, asset.financial_year, asset.asset_state)
  with conn.cursor() as cur:
        cur.execute(q.get_sql())
        results = cur.fetchall()
  list_ = []
  data = []
  columns = ["serial_no", "asset_name", "model", "asset_make", "department", "asset_location", "asset_type", "entry_date", "quantity", "purchase_order_no", "financial_year", "asset_state"]
  for i in results:
      for j in i:
        list_.append(str(i[j]))
      data.append(list_.copy())
      list_.clear()
  return {"column_name" : columns, "values" : data}
