from fastapi import HTTPException, Request
from pypika import PostgreSQLQuery as Query, Table, Criterion
from db.connect import conn
from fastapi import APIRouter
import threading
import os
from models.db import Asset
from models.email import send_email_

router = APIRouter()

origins = [
    "http://localhost:3000",
]


def save_asset_pic(pic, FILE_NAME):
    ASSETS_PATH = "static/assets/"
    if not os.path.exists(ASSETS_PATH):
        os.makedirs(ASSETS_PATH)
    file_path = os.path.join(ASSETS_PATH, FILE_NAME)
    with open(file_path, "wb") as buffer:
        buffer.write(pic)


async def get_asset_dict(req: Request):
    formData = await req.form()
    asset = dict()
    pic = None
    for key in formData.keys():
        if formData.get(key) == "":
            asset[key] = None
            continue
        elif key == "picture":
            pic = await formData.get(key).read()
        else:
            asset[key] = formData.get(key)
    FILE_NAME = asset["serial_no"] + ".png"
    return asset, pic, FILE_NAME


@router.post("/add-asset")
async def add_asset(req: Request):
    asset, pic, FILE_NAME = await get_asset_dict(req)
    try:
        asset_table = Table("asset")
        q = Query.into("asset").insert(
            *asset.values(),
        )
        q1 = (
            Query.from_(asset_table)
            .select(asset_table.star)
            .where(asset_table.serial_no == asset["serial_no"])
        )
        with conn.cursor() as cur:
            cur.execute(q.get_sql())
        conn.commit()

        with conn.cursor() as cur:
            cur.execute(q1.get_sql())
            result = cur.fetchone()

        if pic:
            save_asset_pic(pic, FILE_NAME)

        result_str = ""
        for i in result:
            result_str += i + " : " + str(result[i]) + "<br>"

        subject = "Asset Added"
        body = (
            "Dear Admin,<br> The asset with the following details has been added. <br>"
            + result_str
        )
        threading.Thread(target=send_email_, args=[subject, body], daemon=False).start()
        return {"detail": "Asset Added Successfully"}

    except Exception as e:
        print(e)
        conn.rollback()
        raise HTTPException(404, str(e).split("\n")[1])


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
        q = Query.from_(asset).delete().where(asset.serial_no == serial_no)
        with conn.cursor() as cur:
            cur.execute(q1.get_sql())
            result = cur.fetchone()
            cur.execute(q.get_sql())
        conn.commit()
        print(result)
        if result == None:
            return {"status_code": 404, "detail": "DETAIL: Asset Does Not Exist"}

        result_str = ""
        for i in result:
            result_str += i + " : " + str(result[i]) + "<br>"

        subject = "Asset Deleted"
        body = (
            "Dear Admin,<br> The asset with the following details has been deleted. <br>"
            + result_str
        )
        threading.Thread(target=send_email_, args=[subject, body], daemon=False).start()
        return {"detail": "Asset Deleted Successfully"}

    except Exception as e:
        print(e)
        raise HTTPException(404, str(e).split("\n")[1])


@router.put("/update-asset/")
async def update_asset(req: Request):
    asset, pic, FILE_NAME = await get_asset_dict(req)
    try:
        asset_table = Table("asset")
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
            result = cur.fetchone()
        conn.commit()

        if result == None:
            return {"status_code": 404, "detail": "DETAIL: Asset Does Not Exist"}

        if pic:
            save_asset_pic(pic, FILE_NAME)

        if result == None:
            return {"status_code": 404, "detail": "DETAIL: Asset Does Not Exist"}

        result_str = ""
        for i in result:
            result_str += i + " : " + str(result[i]) + "<br>"

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


@router.post("/get-asset")
def filter_asset(asset_: Asset):
    try:
        asset = Table("asset")

        q = (
            Query.from_(asset)
            .select(
                asset.serial_no,
                asset.asset_name,
                asset.purchase_order_no,
                asset.financial_year,
                asset.asset_holder,
            )
            .where(
                Criterion.all(
                    [asset[k].ilike(f"%{v}%") for k, v in asset_.items() if v != None]
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


@router.get("/get-all-asset")
def get_all_asset():
    asset = Table("asset")
    q = Query.from_(asset).select(asset.star)
    with conn.cursor() as cur:
        cur.execute(q.get_sql())
        results = cur.fetchall()
    list_ = []
    data = []
    columns = list(Asset.__fields__.keys())

    for i in results:
        for j in i:
            list_.append(str(i[j]))
        data.append(list_.copy())
        list_.clear()
    return {"column_name": columns, "values": data}
