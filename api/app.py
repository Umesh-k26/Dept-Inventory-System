from fastapi import Depends, FastAPI, HTTPException, status
from fastapi import Body, Form
from fastapi.middleware.cors import CORSMiddleware
from functools import wraps
from pydantic import BaseModel
from typing import Annotated
from auth import get_email
from configs import Config
from pypika import Query, Table, Tuple, Parameter, Criterion

from db.connect import conn
from db.queries import queries

from models.db import User
from models.requests import ReqUser

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

  
@app.post("/add-user")
async def add_user(user_id: Annotated[str, Form()],  user_type: Annotated[str, Form()], gmail: Annotated[str, Form()],  department: Annotated[str, Form()] = None, first_name: Annotated[str,Form()] = None, last_name: Annotated[str, Form()] = None, ):
  try:
    q = Query.into('users').insert(user_id, first_name, last_name, gmail, user_type, department)
    with conn.cursor() as cur:
       cur.execute(q.get_sql())
    conn.commit()
  except Exception as e:
     print(e)
     conn.rollback()
     raise HTTPException(400, "Cant add user")

@app.get("/get-user/{user_id}")
def get_user(user_id : str) -> User:
  try:
    users = Table('users')
    q = Query.from_(users).select(users.star).where(users.user_id == user_id)
    with conn.cursor() as cur:
        cur.execute(q.get_sql())
        user = cur.fetchall()
  except Exception as e:
    print(e)
    raise HTTPException(201, "User not found")
  return User.parse_obj(user[0])

@app.get("/get-user")
def filter_user(user_type: Annotated[str | None, Query()] = None, gmail: Annotated[str | None, Query()] = None, department: Annotated[str | None, Query()] = None, first_name: Annotated[str | None, Query()] = None, last_name: Annotated[str | None, Query()] = None) -> list[User]:
  try:
    users = Table('users')
    criterion_list = []
    if user_type:
      criterion_list.append(users.user_type == user_type)
    if gmail:
      criterion_list.append(users.gmail == gmail)
    if department:
      criterion_list.append(users.department == department)
    if first_name:
      criterion_list.append(users.first_name.ilike(f'%{first_name}%'))
    if last_name:
      criterion_list.append(users.last_name.ilike(f'%{first_name}%'))

    q = Query.from_(users).select(users.star).where(
      Criterion.all(criterion_list)
    )
    with conn.cursor() as cur:
        cur.execute(q.get_sql())
        results = cur.fetchall()

  except Exception as e:
    print(e)
    raise HTTPException(201, "filters not found")

  return [User.parse_obj(user) for user in results]