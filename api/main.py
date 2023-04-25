from fastapi import Depends, FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from utils.auth import get_email
from utils.configs import Config
import psycopg2
from psycopg2.extras import RealDictCursor
import schedule
import time
import threading
from routes import user, order, asset, bulk_asset
from utils.warranty import warranty_
from db.connect import conn
import uvicorn

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


# scheduling the warranty
def run_on_startup():
    schedule.every().day.at("08:00").do(warranty_)
    while True:
        schedule.run_pending()
        time.sleep(1)


@app.on_event("startup")
def startup_event():
    threading.Thread(target=run_on_startup, daemon=True).start()


@app.get("/get-role/")
async def get_test(details: Annotated[dict, Depends(get_email)]):
    return details


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
app.include_router(user.router)

# Asset Details
app.include_router(asset.router)

# Bulk Asset Details
app.include_router(bulk_asset.router)

# Order Details
app.include_router(order.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
