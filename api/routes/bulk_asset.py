from fastapi import HTTPException, Request
from pypika import PostgreSQLQuery as Query, Table, Criterion
from db.connect import conn
from fastapi import APIRouter
import threading
import os
from models.db import Bulk_Asset
from models.email import send_email_

router = APIRouter()

origins = [
    "http://localhost:3000",
]


def save_asset_pic(pic, FILE_NAME):
    ASSETS_PATH = "static/bulk_assets/"
    if not os.path.exists(ASSETS_PATH):
        os.makedirs(ASSETS_PATH)
    file_path = os.path.join(ASSETS_PATH, FILE_NAME)
    with open(file_path, "wb") as buffer:
        buffer.write(pic)


async def get_asset_dict(req: Request):
    formData = await req.form()
    asset = dict()
    for key in formData.keys():
        if formData.get(key) == "":
            asset[key] = None
            continue
        elif key == "picture":
            pic = await formData.get(key).read()
            FILE_NAME = asset["serial_no"] + ".png"
            if pic:
                save_asset_pic(pic, FILE_NAME)
        else:
            asset[key] = formData.get(key)
    return asset


@router.post("/add-bulk-asset")
async def add_bulk_asset(req: Request):
    asset = await get_asset_dict(req)
    try:
        asset_ = Table("bulk_asset")
        q = Query.into("bulk_asset").insert(
            *asset.values(),
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
        return {"detail": "Asset added Successfully"}

    except Exception as e:
        print(e)
        conn.rollback()
        raise HTTPException(404, str(e).split("\n")[1])


@router.delete("/delete-bulk-asset/{serial_no}/{asset_location}")
async def delete_bulk_asset(serial_no: str, asset_location: str):
    try:
        asset = Table("bulk_asset")
        q1 = (
            Query.from_(asset)
            .select(
                asset.serial_no, asset.asset_name, asset.model, asset.asset_location
            )
            .where(
                asset.serial_no == serial_no and asset.asset_location == asset_location
            )
        )
        q = (
            Query.from_(asset)
            .delete()
            .where(
                asset.serial_no == serial_no and asset.asset_location == asset_location
            )
        )
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
        return {"detail": "Asset deleted Successfully"}

    except Exception as e:
        print(e)
        raise HTTPException(404, str(e).split("\n")[1])


@router.put("/update-bulk-asset/")
async def update_bulk_asset(req: Request):
    asset = await get_asset_dict(req)
    try:
        asset_table = Table("bulk_asset")
        q = Query.update(asset_table).where(asset_table.serial_no == asset["serial_no"])
        for k, v in asset.items():
            if asset[k] is not None:
                q = q.set(k, v)
        q1 = (
            Query.from_(asset_table)
            .select(asset_table.star)
            .where(asset_table.serial_no == asset["serial_no"])
        )

        with conn.cursor() as cur:
            cur.execute(q.get_sql())
            cur.execute(q1.get_sql())
            result = cur.fetchall()
        conn.commit()

        result_str = ""
        for i in result[0]:
            result_str += i + " : " + str(result[0][i]) + "<br>"

        subject = "Asset Updated"
        body = (
            "Dear Admin,<br> The asset with the following details has been updated. <br>"
            + result_str
        )
        threading.Thread(target=send_email_, args=[subject, body], daemon=False).start()
        return {"detail": "Asset Updated Successfully"}

    except Exception as e:
        print(e)
        conn.rollback()
        raise HTTPException(404, str(e).split("\n")[1])


@router.post("/get-bulk-asset")
def filter_asset(asset_: Bulk_Asset):
    try:
        asset = Table("bulk_asset")

        q = (
            Query.from_(asset)
            .select(
                asset.serial_no,
                asset.asset_name,
                asset.asset_location,
                asset.purchase_order_no,
                asset.financial_year,
                asset.quantity,
            )
            .where(
                Criterion.all(
                    [
                        asset[k].ilike(f"%{v}%")
                        for k, v in asset_.dict().items()
                        if v != None
                    ]
                )
            )
        )
        with conn.cursor() as cur:
            cur.execute(q.get_sql())
            asset_details = cur.fetchall()

        s_no = []
        details = []

        for i in asset_details:
            temp = ""
            for j in i:
                if j == "serial_no":
                    s_no.append(i[j])
                else:
                    temp += str(j) + ": " + str(i[j]) + " , "

            details.append(temp[:-3])
        return [s_no, details]

    except Exception as e:
        print(e)
        raise HTTPException(404, str(e).split("\n")[1])


@router.get("/get-all-bulk-asset")
async def get_all_bulk_asset():
    asset = Table("bulk_asset")
    q = Query.from_(asset).select(asset.star)
    with conn.cursor() as cur:
        cur.execute(q.get_sql())
        results = cur.fetchall()
    list_ = []
    data = []
    columns = list(Bulk_Asset.__fields__.keys())
    for i in results:
        for j in i:
            list_.append(str(i[j]))
        data.append(list_.copy())
        list_.clear()
    return {"column_name": columns, "values": data}
