from fastapi import Depends, HTTPException
from typing import Annotated
from auth import get_email
from configs import Config
from pypika import PostgreSQLQuery as Query, Table, Criterion

from db.connect import conn

from models.db import User
from fastapi import APIRouter

from models.email import email, conf
from fastapi_mail import  FastMail, MessageSchema, MessageType

router_user = APIRouter()

origins = [
    "http://localhost:3000",
]

# USER details

@router_user.post("/add-user")
async def add_user(user : User, email_: Annotated[str, Depends(get_email)]):
  try:
    users = Table('users')
    q = Query.into(users).insert(user.user_id, user.first_name, user.last_name, user.email, user.user_type, user.department).on_conflict(users.user_id).do_update(users.user_state, 'Active')
    q1 = Query.from_(users).select(users.star).where(users.user_id == user.user_id)

    with conn.cursor() as cur:
       cur.execute(q.get_sql())
    conn.commit()

    with conn.cursor() as cur:
       cur.execute(q1.get_sql())
       result = cur.fetchall()

    result_str = ''
    for i in result[0]:
      result_str += i + " : " + str(result[0][i]) + "<br>"

    message = MessageSchema(
        subject="User Added",
        recipients=email.dict().get("email"),
        body="Dear Admin,<br> The user with the following details has been added. <br>" + result_str,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)

  except Exception as e:
     print(e)
     conn.rollback()
     raise HTTPException(400, "Cant add user")
  return {"detail": "user added"}
  
  

@router_user.delete("/delete-user/{user_id}")
async def delete_user(user_id: str, email_: Annotated[str, Depends(get_email)]):
  try:
    users = Table('users')
    q1 = Query.from_(users).select(users.star).where(users.user_id == user_id)
    q = Query.update(users).where(users.user_id.ilike(f'{user_id}')).set(users.user_state, 'Inactive')
    with conn.cursor() as cur:
        cur.execute(q.get_sql())
    conn.commit()
    with conn.cursor() as cur:
      cur.execute(q1.get_sql())
      result = cur.fetchall()
    
    result_str = ''
    for i in result[0]:
      result_str += i + " : " + str(result[0][i]) + "<br>"

    message = MessageSchema(
        subject="User Deleted",
        recipients=email.dict().get("email"),
        body="Dear Admin,<br> The user with the following details has been deleted(Inactivated). <br>" + result_str,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)

  except Exception as e:
    print(e)
    raise HTTPException(201, "User not found")
  return {"detail" : "user deleted"}

@router_user.put("/update-user/")
async def update_user(user : User, email_: Annotated[str, Depends(get_email)]):
  try:
    users = Table('users')
    q = Query.update(users).where(users.user_id == user.user_id)
    q1 = Query.from_(users).select(users.star).where(users.user_id == user.user_id)
    set_list = {}
    if user.user_type:
      set_list[users.user_type] = user.user_type
    if user.email:
      set_list[users.email] = user.email
    if user.department:
      set_list[users.department] = user.department
    if user.first_name:
      set_list[users.first_name] = user.first_name
    if user.last_name:
      set_list[users.last_name] = user.last_name
    for k in set_list.keys():
      q = q.set(k, set_list[k])
    with conn.cursor() as cur:
       cur.execute(q.get_sql())
       cur.execute(q1.get_sql())
       result = cur.fetchall()
    conn.commit()

    result_str = ''
    for i in result[0]:
      result_str += i + " : " + str(result[0][i]) + "<br>"

    message = MessageSchema(
        subject="User Updated",
        recipients=email.dict().get("email"),
        body="Dear Admin,<br> The user with the following details has been updated. <br>" + result_str,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)

  except Exception as e:
     print(e)
     conn.rollback()
     raise HTTPException(400, "Cant update user")
  return {"detail" : "User Updated"}


@router_user.get("/get-user/{user_id}")
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


@router_user.post("/get-user")
def filter_user(user : User, email_: Annotated[str, Depends(get_email)]) -> list[User]:
  try:
    users = Table('users')
    q = Query.from_(users).select(users.star)
    criterion_list = []
    if user.user_id:
      criterion_list.append(users.user_id.ilike(f'%{user.user_id}%'))
    if user.user_type:
      criterion_list.append(users.user_type.ilike(f'{user.user_type}'))
    if user.email:
      criterion_list.append(users.email == user.email)
    if user.department:
      criterion_list.append(users.department.ilike(f'%{user.department}%'))
    if user.first_name:
      criterion_list.append(users.first_name.ilike(f'%{user.first_name}%'))
    if user.last_name:
      criterion_list.append(users.last_name.ilike(f'%{user.last_name}%'))
    q = q.where(
      Criterion.all(criterion_list)
    )
    with conn.cursor() as cur:
        cur.execute(q.get_sql())
        results = cur.fetchall()
  except Exception as e:
    print(e)
    raise HTTPException(201, "filters not found")
  return [User.parse_obj(user_) for user_ in results]

@router_user.get("/get-all-user")
async def get_all_user():

    user = Table('users')
    q = Query.from_(user).select(user.star)
    with conn.cursor() as cur:
        cur.execute(q.get_sql())
        results = cur.fetchall()
    list_ = []
    print(results)
    data = []
    columns = ['user_id', 'first_name', 'last_name', 'email', 'user_type', 'department', 'user_state']
    for i in results:
        for j in i:
          print(i[j])
          list_.append(i[j])
          print(list_)
        data.append(list_.copy())
        list_.clear()
    # columns.append(data.copy())
    print(columns)
    return {"column_name" : columns, "values" : data}