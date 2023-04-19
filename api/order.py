from fastapi import HTTPException
from pypika import PostgreSQLQuery as Query, Table, Criterion
from pypika import functions as fn

from db.connect import conn

from fastapi import APIRouter


from models.db import Order_Table
from models.responses import OrderDetails

from models.email import email, conf 
from fastapi_mail import  FastMail, MessageSchema, MessageType

router_order = APIRouter()

origins = [
    "http://localhost:3000",
]


#ORDER details

@router_order.post("/add-order")
async def add_order(order : Order_Table):
  try:
    print(order)
    orders = Table('order_table')
    q = Query.into('order_table').insert(order.purchase_order_no, order.order_date, order.indentor, order.firm_name, order.financial_year, order.final_procurement_date, order.invoice_no, order.invoice_date, order.total_price, order.source_of_fund, order.fund_info, order.other_details)
    with conn.cursor() as cur:
       cur.execute(q.get_sql())
    conn.commit()

    q1 = Query.from_(orders).select(orders.star).where((orders.purchase_order_no == order.purchase_order_no) & (orders.financial_year == order.financial_year))
    with conn.cursor() as cur:
       cur.execute(q1.get_sql())
       result = cur.fetchall()
    result_str = ''
    for i in result[0]:
      result_str += i + " : " + str(result[0][i]) + "<br>"

    message = MessageSchema(
        subject="Order Added",
        recipients=email.dict().get("email"),
        body="Dear Admin,<br> The order with the following details has been added. <br>" + result_str,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)

  except Exception as e:
     print(e)
     conn.rollback()
     raise HTTPException(400, "Cant add order")
  return {"message" : "order added"}
  

@router_order.delete("/delete-order/{purchase_order_no}/{financial_year}")
async def delete_asset(purchase_order_no : str, financial_year : int):
  try:
    order = Table('order_table')
    q1 = Query.from_(order).select(order.star).where((order.purchase_order_no == purchase_order_no) & (order.financial_year == financial_year))
    q = Query.from_(order).delete().where((order.purchase_order_no == purchase_order_no) & (order.financial_year == financial_year))
    with conn.cursor() as cur:
        cur.execute(q1.get_sql())
        result = cur.fetchall()
        cur.execute(q.get_sql())
    conn.commit()

    result_str = ''
    for i in result[0]:
      result_str += i + " : " + str(result[0][i]) + "<br>"

    message = MessageSchema(
        subject="Order Deleted",
        recipients=email.dict().get("email"),
        body="Dear Admin,<br> The order with the following details has been deleted. <br>" + result_str,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)

  except Exception as e:
    print(e)
    raise HTTPException(201, "Order not found")
  return {"message" : "order deleted"}


@router_order.put("/update-order/")
async def update_order(order_ : Order_Table) -> Order_Table:
  try:
    order = Table('order_table')
    q = Query.update(order).where((order.purchase_order_no == order_.purchase_order_no) & (order.financial_year == order_.financial_year))
    q1 = Query.from_(order).select(order.star).where((order.purchase_order_no == order_.purchase_order_no) & (order.financial_year == order_.financial_year))
    set_list = {}
    if order_.order_date:
      set_list['order_date'] = order_.order_date
    if order_.indentor:
      set_list['indentor'] = order_.indentor
    if order_.firm_name:
      set_list['firm_name'] = order_.firm_name
    if order_.final_procurement_date:
      set_list['final_procurement_date'] = order_.final_procurement_date
    if order_.invoice_no:
      set_list['invoice_no'] = order_.invoice_no
    if order_.invoice_date:
      set_list['invoice_date'] = order_.invoice_date
    if order_.total_price:
      set_list['total_price'] = order_.total_price
    if order_.source_of_fund:
      set_list['source_of_fund'] = order_.source_of_fund
    if order_.fund_info:
      set_list['fund_info'] = order_.fund_info
    if order_.other_details:
      set_list['other_details'] = order_.other_details    
    for k in set_list.keys():
      q = q.set(k, set_list[k])
    with conn.cursor() as cur:
       cur.execute(q.get_sql())
       cur.execute(q1.get_sql())
       result = cur.fetchall()
    conn.commit()

    result_str = ''
    for i in result[0]:
      result_str += i + " : " + str(result[0][i]) + "<br>"

    message = MessageSchema(
        subject="Order Updated",
        recipients=email.dict().get("email"),
        body="Dear Admin,<br> The order with the following details has been updated. <br>" + result_str,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)

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

@router_order.get("/get-all-order")
async def get_all_order():

  order = Table('order_table')
  q = Query.from_(order).select(order.star)
  with conn.cursor() as cur:
      cur.execute(q.get_sql())
      results = cur.fetchall()
  list_ = []
  data = []
  column = ['purchase_order_no', 'order_date', 'indentor', 'firm_name', 'financial_year', 'final_procurement_date', 'invoice_no', 'invoice_date', 'total_price', 'source_of_fund', 'fund_info', 'other_details']
  for i in results:
      for j in i:
        list_.append(str(i[j]))
      data.append(list_.copy())
      list_.clear()
  return {"column_name" : column, "values" : data}