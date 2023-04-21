from google.auth.transport import requests
from google.oauth2 import id_token
from starlette.requests import Request
from configs import Config
from db.connect import conn
from pypika import PostgreSQLQuery as Query, Table, Criterion
from fastapi import HTTPException
# TODO: Does Google's verify_auth2_token() function retreive Google's certs every time the function is called? Is there any way to cache the response?

async def db_authorize(email):
  is_admin = False
  try:
    users = Table('users')
    q = Query.from_(users).select(users.star).where(users.email == email)
    with conn.cursor() as cur:
      cur.execute(q.get_sql())
      result = cur.fetchall()
  except Exception as e:
    is_admin = False

  if result:
    if result[0]['user_state'] == "Active":
      if result[0]['user_type'] == "Admin":
        is_admin = True
    else:
      raise HTTPException(404, detail="You are an inactive user. Contact admin to activate you!")
  else:
    raise HTTPException(404, detail="You don't exist in our database. Contact admin to add you.")
  return is_admin
    
async def get_email(request: Request):
    try:
        token = request.headers.get("Authorization")
        idinfo = id_token.verify_oauth2_token(
            token, requests.Request(), Config.GOOGLE_CLIENT_ID
        )
        print(idinfo)
        email = idinfo["email"]

        is_admin = await db_authorize(email)
        print(is_admin)
        if is_admin: 
          return email
        
        raise HTTPException(403, detail="User is not an admin.")

    except HTTPException as e:
      raise e
    except ValueError:
        raise HTTPException(404, detail="We are not able to authenticate you.")
    



# def get_email(conn, token):
#     try:
#         idinfo = id_token.verify_oauth2_token(
#             token, requests.Request(), cnf.GOOGLE_CLIENT_ID
#         )
#         email = idinfo["email"]
#         try:
#             is_admin = queries.get_admin_status_team_member(conn, email=email)[
#                 "is_admin"
#             ]
#         except IndexError:
#             is_admin = False
#         if is_admin:
#             return email
#         return False
#     except ValueError:
#         return None