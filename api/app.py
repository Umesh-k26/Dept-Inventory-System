from fastapi import Depends, FastAPI, HTTPException, status
from fastapi import Body
from fastapi.middleware.cors import CORSMiddleware
from functools import wraps
from pydantic import BaseModel
from typing import Annotated
from auth import get_email
from configs import Config

from db.connect import conn
from db.queries import queries

from models.db import Person
from models.responses import PersonList

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

@app.post("/add-person")
def add_person(person_name: Annotated[str, Body()], person_age: Annotated[int, Body()]):
    try:
      print(person_name, person_age)
      queries.add_person(conn, person_name=person_name, person_age=person_age)
      conn.commit()
    except Exception as e:
      print(e)
      conn.rollback()
      raise HTTPException(400, "Cant add user")
  

@app.get("/get-person/{person_name}")
def get_person(person_name: str) -> list[Person]:
  try:
      result = queries.get_person(conn, person_name=person_name)
  except Exception as e:
    print(e)
    raise HTTPException(201, "Cant get user")
  return [Person.parse_obj(person) for person in result]