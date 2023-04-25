from fastapi import HTTPException
from pypika import PostgreSQLQuery as Query, Table, Criterion
from pypika import functions as fn

from db.connect import conn

from fastapi import APIRouter


from models.db import Order_Table
from models.responses import OrderDetails

from models.email import send_email_

import threading

router = APIRouter()

origins = [
    "http://localhost:3000",
]


@router.post("/add-order")
async def add_order(order: Order_Table):
    try:
        orders = Table("order_table")
        q = Query.into("order_table").insert(*order.dict().values())
        with conn.cursor() as cur:
            cur.execute(q.get_sql())
        conn.commit()

        q1 = (
            Query.from_(orders)
            .select(orders.star)
            .where(
                (orders.purchase_order_no == order.purchase_order_no)
                & (orders.financial_year == order.financial_year)
            )
        )
        with conn.cursor() as cur:
            cur.execute(q1.get_sql())
            result = cur.fetchall()
        result_str = ""
        for i in result[0]:
            result_str += i + " : " + str(result[0][i]) + "<br>"

        subject = "Order Added"
        body = (
            "Dear Admin,<br> The order with the following details has been added. <br>"
            + result_str
        )
        threading.Thread(target=send_email_, args=[subject, body], daemon=False).start()

    except Exception as e:
        print(e)
        conn.rollback()
        raise HTTPException(400, "Cant add order")
    return {"detail": "order added"}


@router.delete("/delete-order/{purchase_order_no}/{financial_year}")
async def delete_asset(purchase_order_no: str, financial_year: int):
    try:
        order = Table("order_table")
        q1 = (
            Query.from_(order)
            .select(order.star)
            .where(
                (order.purchase_order_no == purchase_order_no)
                & (order.financial_year == financial_year)
            )
        )
        q = (
            Query.from_(order)
            .delete()
            .where(
                (order.purchase_order_no == purchase_order_no)
                & (order.financial_year == financial_year)
            )
        )
        with conn.cursor() as cur:
            cur.execute(q1.get_sql())
            result = cur.fetchall()
            cur.execute(q.get_sql())
        conn.commit()

        result_str = ""
        for i in result[0]:
            result_str += i + " : " + str(result[0][i]) + "<br>"

        subject = "Order Deleted"
        body = (
            "Dear Admin,<br> The order with the following details has been deleted. <br>"
            + result_str
        )
        threading.Thread(target=send_email_, args=[subject, body], daemon=False).start()

    except Exception as e:
        print(e)
        raise HTTPException(201, "Order not found")
    return {"detail": "order deleted"}


@router.put("/update-order/")
async def update_order(order_: Order_Table):
    try:
        order = Table("order_table")
        q = Query.update(order).where(
            (order.purchase_order_no == order_.purchase_order_no)
            & (order.financial_year == order_.financial_year)
        )
        for k, v in order_.dict(exclude_none=True, exclude_defaults=True).items():
            q = q.set(k, v)
        q1 = (
            Query.from_(order)
            .select(order.star)
            .where(
                (order.purchase_order_no == order_.purchase_order_no)
                & (order.financial_year == order_.financial_year)
            )
        )
        with conn.cursor() as cur:
            cur.execute(q.get_sql())
            cur.execute(q1.get_sql())
            result = cur.fetchall()
        conn.commit()

        result_str = ""
        for i in result[0]:
            result_str += i + " : " + str(result[0][i]) + "<br>"

        subject = "Order Updated"
        body = (
            "Dear Admin,<br> The order with the following details has been updated. <br>"
            + result_str
        )
        threading.Thread(target=send_email_, args=[subject, body], daemon=False).start()

    except Exception as e:
        print(e)
        conn.rollback()
        raise HTTPException(400, "Cant update order")
    return {"detail": "Order Updated"}


@router.post("/get-order/")
async def get_order(order_: Order_Table) -> list[OrderDetails]:
    try:
        order = Table("order_table")
        user = Table("users")
        asset = Table("asset")
        q = (
            Query.from_(order)
            .select(order.star)
            .where(
                Criterion.all(
                    [
                        order[k].ilike(f"%{v}%")
                        for k, v in order_.dict(
                            exclude_none=True, exclude_defaults=True, exclude_unset=True
                        ).items()
                    ]
                )
            )
        )
        with conn.cursor() as cur:
            cur.execute(q.get_sql())
            order_details = cur.fetchall()
        asset_list = set([i["purchase_order_no"] for i in order_details])
        user_list = set([i["indentor"] for i in order_details])
        q1 = (
            Query.from_(asset)
            .select(
                asset.purchase_order_no,
                asset.asset_name,
                fn.Count(asset.asset_name).as_("quantity"),
            )
            .where(Criterion.any(asset.purchase_order_no == i for i in asset_list))
            .groupby(asset.purchase_order_no, asset.asset_name)
            .orderby("quantity")
        )
        q2 = (
            Query.from_(user)
            .select(user.user_id, user.first_name, user.last_name)
            .where(Criterion.any(user.user_id == i for i in user_list))
        )
        with conn.cursor() as cur:
            cur.execute(q1.get_sql())
            asset_details = cur.fetchall()
            cur.execute(q2.get_sql())
            user_details = cur.fetchall()
        _ = {}
        _["purchase_order_no"] = None
        asset_details_ = {}
        final_list = []
        for i in asset_details:
            if _["purchase_order_no"] != i["purchase_order_no"]:
                asset_details_["asset_details"] = _.copy()
                final_list.append(asset_details_.copy())
                _.clear()
                _["purchase_order_no"] = i["purchase_order_no"]
                _[i["asset_name"]] = i["quantity"]
            else:
                _[i["asset_name"]] = i["quantity"]
        asset_details_["asset_details"] = _.copy()
        final_list.append(asset_details_.copy())
        for i in order_details:
            for j in final_list:
                for k in j.values():
                    if i["purchase_order_no"] == k["purchase_order_no"]:
                        i.update(j)
            for j in user_details:
                if i["indentor"] == j["user_id"]:
                    i.update(j)
        conn.commit()
    except Exception as e:
        print(e)
        raise HTTPException(201, "Order not found")
    return [OrderDetails.parse_obj(_order) for _order in order_details]


@router.get("/get-all-order")
async def get_all_order():
    order = Table("order_table")
    q = Query.from_(order).select(order.star)
    with conn.cursor() as cur:
        cur.execute(q.get_sql())
        results = cur.fetchall()
    list_ = []
    data = []
    column = [
        "purchase_order_no",
        "order_date",
        "indentor",
        "firm_name",
        "financial_year",
        "final_procurement_date",
        "invoice_no",
        "invoice_date",
        "total_price",
        "source_of_fund",
        "fund_info",
        "other_details",
    ]
    for i in results:
        for j in i:
            list_.append(str(i[j]))
        data.append(list_.copy())
        list_.clear()
    return {"column_name": column, "values": data}
