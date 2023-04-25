from fastapi import HTTPException, Request
from pypika import PostgreSQLQuery as Query, Table, Criterion
from psycopg2 import Binary
from db.connect import conn

from models.db import Asset
from models.responses import AssetDetails

from fastapi import APIRouter

from models.email import send_email_

import threading

router = APIRouter()

origins = [
    "http://localhost:3000",
]


@router.post("/add-asset")
async def add_asset(req: Request):
    formData = await req.form()

    asset = dict()
    for key in formData.keys():
        if formData.get(key) == "":
            asset[key] = None
        else:
            asset[key] = formData.get(key)
    if asset["picture"] is not None:
        pic = await asset["picture"].read()
        pic = Binary(pic)
    else:
        pic = None
    if "picture" in asset.keys():
        asset.pop("picture")
    try:
        asset_ = Table("asset")
        q = Query.into("asset").insert(
            *asset.values(),
            pic,
        )
        q1 = (
            Query.from_(asset_)
            .select(asset_.star)
            .where(asset_.serial_no == asset["serial_no"])
        )
        with conn.cursor() as cur:
            cur.execute(q.get_sql())
        conn.commit()

        with conn.cursor() as cur:
            cur.execute(q1.get_sql())
            result = cur.fetchall()

        result_str = ""
        for i in result[0]:
            if i != "picture":
                result_str += i + " : " + str(result[0][i]) + "<br>"

        subject = "Asset Added"
        body = (
            "Dear Admin,<br> The asset with the following details has been added. <br>"
            + result_str
        )
        threading.Thread(target=send_email_, args=[subject, body], daemon=False).start()

    except Exception as e:
        print(e)
        conn.rollback()
        raise HTTPException(e)
    return {"detail": "asset added"}


@router.delete("/delete-asset/{serial_no}")
def delete_asset(serial_no: str):
    try:
        asset = Table("asset")
        q1 = (
            Query.from_(asset)
            .select(
                asset.serial_no,
                asset.asset_name,
                asset.model,
                asset.asset_location,
                asset.asset_holder,
            )
            .where(asset.serial_no == serial_no)
        )
        q = Query.from_(asset).delete().where(asset.serial_no.ilike(f"{serial_no}"))
        with conn.cursor() as cur:
            cur.execute(q1.get_sql())
            result = cur.fetchall()
            cur.execute(q.get_sql())
        conn.commit()

        result_str = ""
        for i in result[0]:
            if i != "picture":
                result_str += i + " : " + str(result[0][i]) + "<br>"

        subject = "Asset Deleted"
        body = (
            "Dear Admin,<br> The asset with the following details has been deleted. <br>"
            + result_str
        )
        threading.Thread(target=send_email_, args=[subject, body], daemon=False).start()

    except Exception as e:
        print(e)
        raise HTTPException(201, "Asset not found")
    return {"detail": "asset deleted"}


@router.put("/update-asset/")
async def update_asset(req: Request):
    formData = await req.form()

    asset_ = dict()
    for key in formData.keys():
        if formData.get(key) == "":
            asset_[key] = None
        else:
            asset_[key] = formData.get(key)

    if asset_["picture"] is not None:
        pic = await asset_["picture"].read()
        pic = Binary(pic)
    else:
        pic = None

    try:
        asset = Table("asset")
        q = Query.update(asset).where(asset.serial_no == asset_["serial_no"])
        for k, v in asset_.items():
            if asset_[k] is not None:
                q = q.set(k, v)
        q1 = (
            Query.from_(asset)
            .select(asset.star)
            .where(asset.serial_no == asset_["serial_no"])
        )

        with conn.cursor() as cur:
            cur.execute(q.get_sql())
            cur.execute(q1.get_sql())
            result = cur.fetchall()
        conn.commit()

        result_str = ""
        for i in result[0]:
            if i != "picture":
                result_str += i + " : " + str(result[0][i]) + "<br>"

        subject = "Asset Updated"
        body = (
            "Dear Admin,<br> The asset with the following details has been updated. <br>"
            + result_str
        )
        threading.Thread(target=send_email_, args=[subject, body], daemon=False).start()

    except Exception as e:
        print(e)
        conn.rollback()
        raise HTTPException(400, "Cant update asset")
    return {"detail": "Asset Updated"}


@router.post("/get-asset")
# def filter_asset(asset_: Asset) -> list[AssetDetails]:
def filter_asset(asset_: Asset):
    try:
        # user = Table("users")
        asset = Table("asset")
        # order = Table("order_table")

        q = (
            Query.from_(asset)
            .select(asset.serial_no, asset.asset_name)
            .where(
                Criterion.all(
                    [
                        asset[k].ilike(f"%{v}%")
                        for k, v in asset_.dict(
                            exclude_none=True, exclude_defaults=True, exclude_unset=True
                        ).items()
                    ]
                )
            )
        )
        with conn.cursor() as cur:
            cur.execute(q.get_sql())
            asset_details = cur.fetchall()
        return asset_details
        # order_list = set([i["purchase_order_no"] for i in asset_details])
        # user_list = set([i["asset_holder"] for i in asset_details])
        # q1 = (
        #     Query.from_(order)
        #     .select(order.star)
        #     .where(Criterion.any(order.purchase_order_no == i for i in order_list))
        # )
        # q2 = (
        #     Query.from_(user)
        #     .select(user.user_id, user.first_name, user.last_name)
        #     .where(Criterion.any(user.user_id == i for i in user_list))
        # )
        # with conn.cursor() as cur:
        #     cur.execute(q1.get_sql())
        #     order_details = cur.fetchall()
        #     cur.execute(q2.get_sql())
        #     user_details = cur.fetchall()
        # for i in asset_details:
        #     for j in order_details:
        #         if i["purchase_order_no"] == j["purchase_order_no"]:
        #             i.update(j)
        #     for j in user_details:
        #         if i["asset_holder"] == j["user_id"]:
        #             i.update(j)
    except Exception as e:
        print(e)
        raise HTTPException(201, "filters not found")

    # return [AssetDetails.parse_obj(asset) for asset in asset_details]


@router.get("/get-all-asset")
def get_all_asset():
    asset = Table("asset")
    q = Query.from_(asset).select(
        asset.serial_no,
        asset.asset_name,
        asset.model,
        asset.asset_make,
        asset.department,
        asset.asset_location,
        asset.asset_holder,
        asset.asset_type,
        asset.entry_date,
        asset.warranty,
        asset.is_hardware,
        asset.system_no,
        asset.purchase_order_no,
        asset.financial_year,
        asset.asset_state,
    )
    with conn.cursor() as cur:
        cur.execute(q.get_sql())
        results = cur.fetchall()
    list_ = []
    data = []
    columns = [
        "serial_no",
        "asset_name",
        "model",
        "asset_make",
        "department",
        "asset_location",
        "asset_holder",
        "asset_type",
        "entry_date",
        "warranty",
        "is_hardware",
        "system_no",
        "purchase_order_no",
        "financial_year",
        "asset_state",
    ]
    for i in results:
        for j in i:
            list_.append(str(i[j]))
        data.append(list_.copy())
        list_.clear()
    return {"column_name": columns, "values": data}
