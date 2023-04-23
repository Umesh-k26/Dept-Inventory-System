from pydantic import BaseModel
import datetime


class AssetDetails(BaseModel):
    asset_name: str | None = None
    model: str | None = None
    serial_no: str
    department: str | None = None
    asset_location: str | None = None
    entry_date: datetime.date | None = None
    unit_price: float | None = None
    warranty: datetime.date | None = None
    is_hardware: str | None = None
    system_no: str | None = None
    purchase_order_no: str | None = None
    asset_state: str | None = None
    # picture : str | None = None #subject to change once we find the proper one
    order_date: datetime.date | None = None
    indentor: str | None = None
    firm_name: str | None = None
    financial_year: int | None = None
    # quantity : int
    gst_tin: str | None = None
    final_procurement_date: datetime.date | None = None
    invoice_no: str
    invoice_date: datetime.date | None = None
    user_id: str
    first_name: str | None = None
    last_name: str | None = None


class OrderDetails(BaseModel):
    purchase_order_no: str | None = None  # primary key
    order_date: datetime.date | None = None
    indentor: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    firm_name: str | None = None
    financial_year: int | None = None
    gst_tin: str | None = None
    final_procurement_date: datetime.date | None = None
    invoice_no: str | None = None  # primary key
    invoice_date: datetime.date | None = None
    asset_details: dict | None = None
