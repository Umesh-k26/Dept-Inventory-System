from pydantic import BaseModel
from fastapi import UploadFile
import datetime
import json


class User(BaseModel):
    user_id: str | None = None  # primary key
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    user_type: str | None = None
    department: str | None = None
    user_state: str = "Active"


class Asset(BaseModel):
    asset_name: str | None = None
    model: str | None = None
    asset_make: str | None = None
    serial_no: str | None = None  # primary key
    department: str | None = None
    asset_location: str | None = None
    asset_holder: str | None = None
    asset_type: str | None = None
    entry_date: datetime.date | None = None
    warranty: datetime.date | None = None
    is_hardware: str | None = None
    system_no: str | None = None
    purchase_order_no: str | None = None
    financial_year: int | None = None
    asset_state: str | None = None
    picture: UploadFile | None = None

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class Bulk_Asset(BaseModel):
    asset_name: str | None = None
    model: str | None = None
    asset_make: str | None = None
    serial_no: str | None = None  # primary key
    department: str | None = None
    asset_location: str | None = None  # primary key
    asset_type: str | None = None
    entry_date: datetime.date | None = None
    quantity: int | None = None
    purchase_order_no: str | None = None
    financial_year: int | None = None
    asset_state: str | None = None
    picture: UploadFile | None = None


class Order_Table(BaseModel):
    purchase_order_no: str | None = None  # primary key
    order_date: datetime.date | None = None
    indentor: str | None = None
    firm_name: str | None = None
    financial_year: int | None = None  # primary key
    final_procurement_date: datetime.date | None = None
    invoice_no: str | None = None
    invoice_date: datetime.date | None = None
    total_price: float | None = None
    source_of_fund: str | None = None
    fund_info: str | None = None
    other_details: str | None = None
