from pypika import PostgreSQLQuery as Query, Table

from db.connect import conn
import datetime

from models.email import email, conf
from fastapi_mail import FastMail, MessageSchema, MessageType
import asyncio


async def warranty():
    asset = Table("asset")
    q = Query.from_(asset).select(asset.asset_name, asset.serial_no, asset.warranty)
    with conn.cursor() as cur:
        cur.execute(q.get_sql())
        result = cur.fetchall()
    date_today = datetime.date.today()
    data = []
    for i in result:
        if (i["warranty"] - date_today).days == 90:
            data.append(i)
    result_str = ""
    for i in data:
        for j in i:
            result_str += j + " : " + str(i[j]) + "<br>"
        result_str += "<br>"

    message = MessageSchema(
        subject="Warranty expiration",
        recipients=email.dict().get("email"),
        body="Dear Admin,<br> The warranty of the assets with the following details will expire within 90 days.<br>"
        + result_str,
        subtype=MessageType.html,
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    return


def warranty_():
    asyncio.run(warranty())
