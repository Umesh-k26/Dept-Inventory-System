from fastapi import HTTPException
from pypika import PostgreSQLQuery as Query, Table, Criterion
from pypika import functions as fn

from db.connect import conn

from fastapi import APIRouter


from models.db import Order_Table
from models.responses import OrderDetails

router_order = APIRouter()

origins = [
    "http://localhost:3000",
]


#ORDER details

@router_order.post("/add-order")
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
  

@router_order.delete("/delete-order/{purchase_order_no}{invoice_no}")
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


@router_order.put("/update-order/")
async def update_order(order_ : Order_Table) -> Order_Table:
  try:
    order = Table('order_table')
    q = Query.update(order).where(order.purchase_order_no.ilike(f'{order_.purchase_order_no}') & order.invoice_no.ilike(f'{order_.invoice_no}'))
    q1 = Query.from_(order).select(order.star).where(order.purchase_order_no.ilike(f'{order_.purchase_order_no}') & order.invoice_no.ilike(f'{order_.invoice_no}'))
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
       cur.execute(q1.get_sql())
       result = cur.fetchall()
    conn.commit()
  except Exception as e:
     print(e)
     conn.rollback()
     raise HTTPException(400, "Cant update order")
  return Order_Table.parse_obj(result[0])

@router_order.post("/get-order/")
async def get_order(order_ : Order_Table) -> list[OrderDetails]:
  try:
    order = Table('order_table')
    user = Table('users')
    asset = Table('asset')
    criterion_list = []
    if order_.purchase_order_no:
      criterion_list.append(order.purchase_order_no.ilike(f'%{order_.purchase_order_no}%'))
    if order_.order_date:
      criterion_list.append(order.order_date.ilike(f'%{order_.order_date}%'))
    if order_.indentor:
      criterion_list.append(order.indentor.ilike(f'%{order_.indentor}%'))
    if order_.firm_name:
      criterion_list.append(order.firm_name.ilike(f'%{order_.firm_name}%'))
    if order_.financial_year:
      criterion_list.append(order.financial_year.ilike(f'%{order_.financial_year}%'))
    if order_.gst_tin:
      criterion_list.append(order.gst_tin.ilike(f'%{order_.gst_tin}%'))
    if order_.final_procurement_date:
      criterion_list.append(order.final_procurement_date.ilike(f'%{order_.final_procurement_date}%'))
    if order_.invoice_no:
      criterion_list.append(order.invoice_no.ilike(f'%{order_.invoice_no}%'))
    if order_.invoice_date:
      criterion_list.append(order.invoice_date.ilike(f'%{order_.invoice_date}%'))
    q = Query.from_(order).select(order.star).where(
      Criterion.all(criterion_list)
      )
    with conn.cursor() as cur:
        cur.execute(q.get_sql())
        order_details = cur.fetchall()
    asset_list = set([i['purchase_order_no'] for i in order_details])
    user_list = set([i['indentor'] for i in order_details])
    q1 = Query.from_(asset).select(asset.purchase_order_no, asset.asset_name, fn.Count(asset.asset_name).as_('quantity')).where(
      Criterion.any( asset.purchase_order_no == i for i in asset_list)
      ).groupby(asset.purchase_order_no, asset.asset_name).orderby('quantity')
    q2 = Query.from_(user).select(user.user_id, user.first_name, user.last_name).where(
      Criterion.any( user.user_id == i for i in user_list)
      )
    with conn.cursor() as cur:
        cur.execute(q1.get_sql())
        asset_details = cur.fetchall()
        cur.execute(q2.get_sql())
        user_details = cur.fetchall()
    _ = {}
    _['purchase_order_no'] = None
    asset_details_ = {}
    final_list = []
    for i in asset_details:
      if _['purchase_order_no'] != i['purchase_order_no']:
        asset_details_['asset_details'] = _.copy()
        final_list.append(asset_details_.copy())
        _.clear()
        _['purchase_order_no'] = i['purchase_order_no']
        _[i['asset_name']] = i['quantity']
      else:
        _[i['asset_name']] = i['quantity']
    asset_details_['asset_details'] = _.copy()
    final_list.append(asset_details_.copy())
    for i in order_details:
      for j in final_list:
        for k in j.values():
          if i['purchase_order_no'] == k['purchase_order_no']:
            i.update(j)
      for j in user_details:
        if i['indentor'] == j['user_id']:
          i.update(j)
    conn.commit()
  except Exception as e:
    print(e)
    raise HTTPException(201, "Order not found")
  return [OrderDetails.parse_obj(_order) for _order in order_details]