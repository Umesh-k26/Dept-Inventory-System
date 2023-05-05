from google.auth.transport import requests
from google.oauth2 import id_token
from starlette.requests import Request
from utils.configs import Config
from db.connect import conn
from pypika import PostgreSQLQuery as Query, Table, Criterion
from fastapi import HTTPException
from cachetools import TTLCache

# TODO: Does Google's verify_auth2_token() function retreive Google's certs every time the function is called? Is there any way to cache the response?

cache = TTLCache(maxsize=1000, ttl=3600)


async def db_authorize(email):
    details = dict()
    try:
        # print("conn from db_authorize : ", conn)
        users = Table("users")
        q = Query.from_(users).select(users.star).where(users.email == email)
        with conn.cursor() as cur:
            cur.execute(q.get_sql())
            result = cur.fetchone()
    except Exception as e:
        raise e
    if result:
        if result["user_state"] != "Active":
            raise HTTPException(
                404, detail="You are an inactive user. Contact admin to activate you!"
            )
    else:
        raise HTTPException(
            404, detail="You don't exist in our database. Contact admin to add you."
        )
    details["email"] = email
    details["user_type"] = result["user_type"]
    details["user_id"] = result["user_id"]
    return details


async def get_user_details(request: Request):
    print("called get_user_details")
    token = request.headers.get("Authorization")
    for v in cache.values():
        print(v)
    user_info = cache.get(token)
    if user_info:
        return user_info
    else:
        try:
            print("doing auth...")
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), Config.GOOGLE_CLIENT_ID
            )

            email = idinfo["email"]
            user_info = await db_authorize(email)
            cache[token] = user_info
            return user_info

        except HTTPException as e:
            print(e)
            raise e
        except ValueError as e:
            print(e)
            raise HTTPException(404, detail="We are not able to authenticate you.")


async def override_get_user_details(request: Request):
    email = request.headers.get("Authorization")
    return email
