from fastapi import HTTPException
from pypika import PostgreSQLQuery as Query, Table, Criterion
from db.connect import conn
from models.db import User
from fastapi import APIRouter
from models.email import send_email_
import threading

router = APIRouter()

origins = [
    "http://localhost:3000",
]


@router.post("/add-user")
def add_user(user: User):
    # access return value of get_user_details
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
        return {"detail": "User Added Successfully"}

    except Exception as e:
        print(e)
        conn.rollback()
        raise HTTPException(404, str(e).split("\n")[1])


@router.put("/activate-deactivate-user/{user_id}/{user_state}")
def activate_deactivate_user(user_id: str, user_state: str):
    try:
        users = Table("users")
        q1 = Query.from_(users).select(users.star).where(users.user_id == user_id)
        q = Query.update(users).where(users.user_id.ilike(f"{user_id}"))
        if user_state == "Active":
            q = q.set(users.user_state, "Active")
        elif user_state == "Inactive":
            q = q.set(users.user_state, "Inactive")
        with conn.cursor() as cur:
            cur.execute(q.get_sql())
        conn.commit()
        with conn.cursor() as cur:
            cur.execute(q1.get_sql())
            result = cur.fetchone()

        if result == None:
            return {"status_code": 404, "detail": "DETAIL: User Does Not Exist"}

        result_str = ""
        for i in result:
            result_str += i + " : " + str(result[i]) + "<br>"

        subject = "User State Change"
        body = (
            "Dear Admin,<br> The user state of the user with the following details has been changed. <br>"
            + result_str
        )
        threading.Thread(target=send_email_, args=[subject, body], daemon=False).start()
        return {"detail": "User State Changed Successfully"}

    except Exception as e:
        print(e)
        raise HTTPException(404, "DETAIL: User Does Not Exist")


@router.put("/update-user/")
def update_user(user: User):
    try:
        users = Table("users")
        q = Query.update(users).where(users.user_id == user.user_id)
        for k, v in user.dict(exclude_none=True, exclude_defaults=True).items():
            q = q.set(k, v)
        q1 = Query.from_(users).select(users.star).where(users.user_id == user.user_id)

        with conn.cursor() as cur:
            cur.execute(q.get_sql())
            cur.execute(q1.get_sql())
            result = cur.fetchone()
        conn.commit()

        if result == None:
            return {"status_code": 404, "detail": "DETAIL: User Does Not Exist"}

        result_str = ""
        for i in result:
            result_str += i + " : " + str(result[i]) + "<br>"

        subject = "User Updated"
        body = (
            "Dear Admin,<br> The user with the following details has been updated. <br>"
            + result_str
        )
        threading.Thread(target=send_email_, args=[subject, body], daemon=False).start()
        return {"detail": "User Updated Successfully"}

    except Exception as e:
        print(e)
        conn.rollback()
        raise HTTPException(404, str(e).split("\n")[1])


@router.get("/get-user/{user_id}")
def get_user(user_id: str) -> User:
    try:
        users = Table("users")
        q = Query.from_(users).select(users.star).where(users.user_id == user_id)
        with conn.cursor() as cur:
            cur.execute(q.get_sql())
            user = cur.fetchall()
        return User.parse_obj(user[0])

    except Exception as e:
        print(e)
        raise HTTPException(404, str(e).split("\n")[1])


@router.post("/get-user")
def filter_user(user: User) -> list[User]:
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
        return [User.parse_obj(user_) for user_ in results]

    except Exception as e:
        print(e)
        raise HTTPException(404, str(e).split("\n")[1])


@router.get("/get-all-user")
def get_all_user():
    user = Table("users")
    q = Query.from_(user).select(user.star)
    with conn.cursor() as cur:
        cur.execute(q.get_sql())
        results = cur.fetchall()
    list_ = []
    data = []
    columns = list(User.__fields__.keys())
    for i in results:
        for j in i:
            list_.append(i[j])
        data.append(list_.copy())
        list_.clear()
    return {"column_name": columns, "values": data}
