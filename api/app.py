from fastapi import Depends, FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from auth import get_email
from configs import Config
from pypika import PostgreSQLQuery as Query, Table, Tuple, Parameter, Criterion

from db.connect import conn
from psycopg2 import Binary
import cgi

from user import router_user
from asset import router_asset
from order import router_order
from bulk_asset import router_bulk_asset

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


@app.get("/get-role/")
async def get_test(email: Annotated[str ,Depends(get_email)]):
  print("line 33: app.py")
  return {"email": email}

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        # Process the file contents
        return {"filename": file.filename, "status": "success"}
    except Exception as e:
        print(e)
        return {"filename": file.filename, "status": "error", "message": str(e)}


# USER details

app.include_router(router_user)

#Asset Details

app.include_router(router_asset)

#Bulk Asset Details
app.include_router(router_bulk_asset)

#Order Details

app.include_router(router_order)
