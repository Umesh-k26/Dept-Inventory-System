from fastapi import Depends, HTTPException
from typing import Annotated
from utils.auth import get_email
from utils.configs import Config
from pypika import PostgreSQLQuery as Query, Table, Criterion
from db.connect import conn
from fastapi import BackgroundTasks
from models.db import User
from fastapi import APIRouter

from models.email import send_email_

import threading

import threading

router = APIRouter()

origins = [
    "http://localhost:3000",
]

# delete user has to be modified!!


@router.post("/add-user")
def add_user(user: User, email_: Annotated[str, Depends(get_email)]):
    try:
        users = Table("users")
        q = Query.into(users).insert(*user.dict().values())
        q1 = Query.from_(users).select(users.star).where(users.user_id == user.user_id)

        with conn.cursor() as cur:
            cur.execute(q.get_sql())
        conn.commit()

        with conn.cursor() as cur:
            cur.execute(q1.get_sql())
            result = cur.fetchall()

        result_str = ""
        for i in result[0]:
            result_str += i + " : " + str(result[0][i]) + "<br>"

        body = (
            "Dear Admin,<br> The user with the following details has been added. <br>"
            + result_str
        )
        subject = "User Added"
        threading.Thread(target=send_email_, args=[subject, body], daemon=False).start()

    except Exception as e:
        print(e)
        conn.rollback()
        raise HTTPException(400, "Cant add user")
    return {"detail": "user added"}


@router.delete("/delete-user/{user_id}")
async def delete_user(user_id: str, email_: Annotated[str, Depends(get_email)]):
    try:
        users = Table("users")
        q1 = Query.from_(users).select(users.star).where(users.user_id == user_id)
        q = (
            Query.update(users)
            .where(users.user_id.ilike(f"{user_id}"))
            .set(users.user_state, "Inactive")
        )
        with conn.cursor() as cur:
            cur.execute(q.get_sql())
        conn.commit()
        with conn.cursor() as cur:
            cur.execute(q1.get_sql())
            result = cur.fetchall()

        result_str = ""
        for i in result[0]:
            result_str += i + " : " + str(result[0][i]) + "<br>"

        subject = "User Deleted"
        body = (
            "Dear Admin,<br> The user with the following details has been deleted(Inactivated). <br>"
            + result_str
        )
        threading.Thread(target=send_email_, args=[subject, body], daemon=False).start()

    except Exception as e:
        print(e)
        raise HTTPException(201, "User not found")
    return {"detail": "user deleted"}


@router.put("/update-user/")
async def update_user(user: User, email_: Annotated[str, Depends(get_email)]):
    try:
        users = Table("users")
        q = Query.update(users).where(users.user_id == user.user_id)
        for k, v in user.dict(exclude_none=True, exclude_defaults=True).items():
            q = q.set(k, v)
        q1 = Query.from_(users).select(users.star).where(users.user_id == user.user_id)

        with conn.cursor() as cur:
            cur.execute(q.get_sql())
            cur.execute(q1.get_sql())
            result = cur.fetchall()
        conn.commit()

        result_str = ""
        for i in result[0]:
            result_str += i + " : " + str(result[0][i]) + "<br>"

        subject = "User Updated"
        body = (
            "Dear Admin,<br> The user with the following details has been updated. <br>"
            + result_str
        )
        threading.Thread(target=send_email_, args=[subject, body], daemon=False).start()

    except Exception as e:
        print(e)
        conn.rollback()
        raise HTTPException(400, "Cant update user")
    return {"detail": "User Updated"}


@router.get("/get-user/{user_id}")
def get_user(user_id: str) -> User:
    try:
        users = Table("users")
        q = Query.from_(users).select(users.star).where(users.user_id == user_id)
        with conn.cursor() as cur:
            cur.execute(q.get_sql())
            user = cur.fetchall()
    except Exception as e:
        print(e)
        raise HTTPException(201, "User not found")
    return User.parse_obj(user[0])


@router.post("/get-user")
def filter_user(user: User, email_: Annotated[str, Depends(get_email)]) -> list[User]:
    try:
        users = Table("users")
        q = (
            Query.from_(users)
            .select(users.star)
            .where(
                Criterion.all(
                    [
                        users[k].ilike(f"%{v}%")
                        for k, v in user.dict(
                            exclude_none=True, exclude_defaults=True, exclude_unset=True
                        ).items()
                    ]
                )
            )
        )
        with conn.cursor() as cur:
            cur.execute(q.get_sql())
            results = cur.fetchall()
    except Exception as e:
        print(e)
        raise HTTPException(201, "filters not found")
    return [User.parse_obj(user_) for user_ in results]


@router.get("/get-all-user")
async def get_all_user():
    user = Table("users")
    q = Query.from_(user).select(user.star)
    with conn.cursor() as cur:
        cur.execute(q.get_sql())
        results = cur.fetchall()
    list_ = []
    data = []
    columns = [
        "user_id",
        "first_name",
        "last_name",
        "email",
        "user_type",
        "department",
        "user_state",
    ]
    for i in results:
        for j in i:
            list_.append(i[j])
        data.append(list_.copy())
        list_.clear()
    return {"column_name": columns, "values": data}
