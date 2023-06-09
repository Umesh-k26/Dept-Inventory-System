from fastapi import HTTPException, Request, Depends
from fastapi import APIRouter
from pypika import PostgreSQLQuery as Query, Table, Criterion
from pypika import functions as fn
import os
from typing import Annotated
from db.connect import conn
from models.db import Order_Table
from models.responses import OrderDetails
from models.email import send_email_
from utils.auth import get_user_details
import threading

router = APIRouter()

origins = [
    "http://localhost:3000",
]


def save_pdf(pdf, FILE_NAME, file_type):
    if file_type == "invoice":
        PATH = "static/invoices"
    elif file_type == "purchase_order":
        PATH = "static/purchase_order"

    if not os.path.exists(PATH):
        os.makedirs(PATH)
    file_path = os.path.join(PATH, FILE_NAME)
    with open(file_path, "wb") as buffer:
        buffer.write(pdf)


async def get_order_dict(req: Request):
    formData = await req.form()
    order = dict()
    invoice = None
    purchase_order = None
    for key in formData.keys():
        if formData.get(key) == "":
            order[key] = None
            continue
        elif key == "invoice":
            invoice = await formData.get(key).read()
        elif key == "purchase_order":
            purchase_order = await formData.get(key).read()
        else:
            order[key] = formData.get(key)
    FILE_NAME = order["financial_year"] + "_" + order["purchase_order_no"] + ".pdf"
    return order, invoice, purchase_order, FILE_NAME


@router.post("/add-order")
async def add_order(req: Request):
    order, invoice, purchase_order, FILE_NAME = await get_order_dict(req)
    try:
        orders = Table("order_table")
        q = Query.into("order_table").insert(*order.values())
        with conn.cursor() as cur:
            cur.execute(q.get_sql())
        conn.commit()

        q1 = (
            Query.from_(orders)
            .select(orders.star)
            .where(
                (orders.purchase_order_no == order["purchase_order_no"])
                & (orders.financial_year == order["financial_year"])
            )
        )
        with conn.cursor() as cur:
            cur.execute(q1.get_sql())
            result = cur.fetchone()

        if invoice:
            save_pdf(invoice, FILE_NAME, "invoice")
        if purchase_order:
            save_pdf(purchase_order, FILE_NAME, "purchase_order")

        result_str = ""
        for i in result:
            result_str += i + " : " + str(result[i]) + "<br>"

        subject = "Order Added"
        body = (
            "Dear Admin,<br> The order with the following details has been added. <br>"
            + result_str
        )
        threading.Thread(target=send_email_, args=[subject, body], daemon=False).start()
        return {"detail": "Order Added Successfully"}

    except Exception as e:
        print(e)
        conn.rollback()
        raise HTTPException(404, str(e).split("\n")[1])


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
            result = cur.fetchone()
            cur.execute(q.get_sql())
        conn.commit()

        if result == None:
            return {"status_code": 404, "detail": "DETAIL: Order Does Not Exist"}

        result_str = ""
        for i in result:
            result_str += i + " : " + str(result[i]) + "<br>"

        subject = "Order Deleted"
        body = (
            "Dear Admin,<br> The order with the following details has been deleted. <br>"
            + result_str
        )
        threading.Thread(target=send_email_, args=[subject, body], daemon=False).start()
        return {"detail": "Order Deleted Successfully"}

    except Exception as e:
        print(e)
        raise HTTPException(404, str(e).split("\n")[1])


@router.put("/update-order/")
async def update_order(req: Request):
    order, invoice, purchase_order, FILE_NAME = await get_order_dict(req)
    print(order)
    try:
        order_table = Table("order_table")
        q = Query.update(order_table).where(
            (order_table.purchase_order_no == order["purchase_order_no"])
            & (order_table.financial_year == order["financial_year"])
        )
        for k, v in order.items():
            if order[k] is not None:
                q = q.set(k, v)
        q1 = (
            Query.from_(order_table)
            .select(order_table.star)
            .where(
                (order_table.purchase_order_no == order["purchase_order_no"])
                & (order_table.financial_year == order["financial_year"])
            )
        )
        print(str(q))
        with conn.cursor() as cur:
            cur.execute(q.get_sql())
            cur.execute(q1.get_sql())
            result = cur.fetchone()
        conn.commit()

        if result == None:
            return {"status_code": 404, "detail": "DETAIL: Order Does Not Exist"}

        if invoice:
            save_pdf(invoice, FILE_NAME, "invoice")
        if purchase_order:
            save_pdf(purchase_order, FILE_NAME, "purchase_order")

        if result == None:
            return {"status_code": 404, "detail": "DETAIL: Order Does Not Exist"}

        result_str = ""
        for i in result:
            result_str += i + " : " + str(result[i]) + "<br>"

        subject = "Order Updated"
        body = (
            "Dear Admin,<br> The order with the following details has been updated. <br>"
            + result_str
        )
        threading.Thread(target=send_email_, args=[subject, body], daemon=False).start()
        return {"detail": "Order Updated Successfully"}

    except Exception as e:
        print(e)
        conn.rollback()
        raise HTTPException(404, str(e).split("\n"))


@router.post("/get-order/")
async def get_order(order_: Order_Table):
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
        return [OrderDetails.parse_obj(_order) for _order in order_details]

    except Exception as e:
        print(e)
        raise HTTPException(404, str(e).split("\n")[1])


@router.get("/get-all-order")
async def get_all_order(details: Annotated[dict, Depends(get_user_details)]):
    order = Table("order_table")
    q = Query.from_(order).select(order.star)

    if details["user_type"] == "Student":
        q = q.where(order.indentor == details["user_id"])
    with conn.cursor() as cur:
        cur.execute(q.get_sql())
        results = cur.fetchall()
    list_ = []
    data = []
    column = list(Order_Table.__fields__.keys())
    for i in results:
        for j in i:
            list_.append(str(i[j]))
        data.append(list_.copy())
        list_.clear()

    return {"column_name": column, "values": data}
