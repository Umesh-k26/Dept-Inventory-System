from fastapi import Depends, FastAPI, HTTPException, status
from fastapi import Body, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from functools import wraps
from pydantic import BaseModel
from typing import Annotated
from auth import get_email
from configs import Config
from pypika import Query, Table, Tuple, Parameter, Criterion

from db.connect import conn

from models.db import User, Asset, Bulk_Asset, Order_Table
from models.responses import AssetDetails

import datetime

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def get_test(email: Annotated[str, Depends(get_email)]):
    print(f"email is {email}")
    print(Config.GOOGLE_CLIENT_ID)
    return {"email": email}

# USER details

@app.post("/add-user")
async def add_user(user : User):
  try:
    q = Query.into('users').insert(user.user_id, user.first_name, user.last_name, user.gmail, user.user_type, user.department)
    with conn.cursor() as cur:
       cur.execute(q.get_sql())
    conn.commit()
  except Exception as e:
     print(e)
     conn.rollback()
     raise HTTPException(400, "Cant add user")
  return {"message": "user added"}
  

@app.delete("/delete-user/{user_id}")
async def delete_user(user_id: str):
  try:
    users = Table('users')
    q = Query.from_(users).delete().where(users.user_id.ilike(f'{user_id}'))
    with conn.cursor() as cur:
        cur.execute(q.get_sql())
    conn.commit()
  except Exception as e:
    print(e)
    raise HTTPException(201, "User not found")
  return {"message" : "user deleted"}
