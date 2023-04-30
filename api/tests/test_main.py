from fastapi.testclient import TestClient
from main import app
from utils.auth import get_user_details, override_get_user_details
from models.email import send_email_, override_send_email_
import pytest

from models.db import User, Asset, Bulk_Asset, Order_Table


client = TestClient(app)


if __name__ == "__main__":
    app.dependency_overrides[get_user_details] = override_get_user_details
    app.dependency_overrides[send_email_] = override_send_email_
    pytest.main()
    app.dependency_overrides = {}


# User Testing


def test_add_user():
    res = client.post(
        "/add-user",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        json=User(
            user_id="cs20btech11024",
            first_name="Umesh",
            last_name="Kalvakuntla",
            email="cs20btech11024@iith.ac.in",
            department="CSE",
            user_state="Active",
            user_type="Admin",
        ).dict(),
    )
    assert res.status_code == 200

    res = client.post(
        "/add-user",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        json=User(
            user_id="cs20btech11015",
            first_name="Aarthi",
            last_name="Dontha",
            email="cs20btech11015@iith.ac.in",
            department="CSE",
            user_state="Active",
            user_type="Admin",
        ).dict(),
    )
    assert res.status_code == 200

    res = client.post(
        "/add-user",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        json=User(
            user_id="cs20btech11014",
            first_name="Diya",
            last_name=None,
            email="cs20btech11014@iith.ac.in",
            # department="CSE",
            user_state="Active",
            user_type="Admin",
        ).dict(),
    )
    assert res.status_code == 200

    res = client.post(
        "/add-user",
        headers={"Authorization": "cs20btech11007@iith.ac.in"},
        json=User(
            user_id="cs20btech11007",
            first_name="B.Revanth",
            last_name=None,
            email="cs20btech11007@iith.ac.in",
            # department="CSE",
            user_state="Active",
            user_type="Admin",
        ).dict(),
    )
    assert res.status_code == 200

    # same user_id
    res = client.post(
        "/add-user",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        json=User(
            user_id="cs20btech11015",
            first_name="Aarthi",
            last_name="Dontha",
            email="cs20btech11015@iith.ac.in",
            department="CSE",
            user_state="Active",
            user_type="Admin",
        ).dict(),
    )
    assert res.status_code == 404

    # different user_id and same email_id
    res = client.post(
        "/add-user",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        json=User(
            user_id="cs20btech11005",
            first_name="Umesh",
            last_name="Kalvakuntla",
            email="cs20btech11024@iith.ac.in",
            department="CSE",
            user_state="Active",
            user_type="Admin",
        ).dict(),
    )
    assert res.status_code == 404

    # same user_id and same email_id as student
    res = client.post(
        "/add-user",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        json=User(
            user_id="cs20btech11008",
            first_name="Raja",
            last_name="ravi kiran",
            email="cs20btech11008@iith.ac.in",
            department="CSE",
            user_state="Active",
            user_type="student",
        ).dict(),
    )
    assert res.status_code == 200

    res = client.post(
        "/add-user",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        json=User(
            user_id="cs20btech11008",
            first_name="Raja",
            last_name="ravi kiran",
            email="cs20btech11008@iith.ac.in",
            department="CSE",
            user_state="Active",
            user_type="student",
        ).dict(),
    )
    assert res.status_code == 404


def test_update_user():
    res = client.put(
        "/update-user",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        json=User(
            user_id="cs20btech11014",
            last_name="Goyal",
        ).dict(),
    )
    assert res.status_code == 200

    res = client.put(
        "/update-user",
        headers={"Authorization": "cs20btech11007@iith.ac.in"},
        json=User(
            user_id="cs20btech11007",
            last_name="Nayak",
            user_type="stud",
        ).dict(),
    )
    assert res.status_code == 200

    # updating email to already existing email
    res = client.put(
        "/update-user",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        json=User(
            user_id="cs20btech11015",
            email="cs20btech11014@iith.ac.in",
        ).dict(),
    )
    assert res.status_code == 404

    # updating a non existing user
    res = client.put(
        "/update-user",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        json=User(
            user_id="cs20btech11019",
            email="cs20btech11014@iith.ac.in",
        ).dict(),
    )
    assert res.json()["status_code"] == 404


def test_activate_deactivate_user():
    res = client.put(
        "/activate-deactivate-user/cs20btech11024/Inactive",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
    )
    assert res.status_code == 200

    res = client.put(
        "/activate-deactivate-user/cs20btech11024/Active",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
    )
    assert res.status_code == 200

    # invalid user
    res = client.put(
        "/activate-deactivate-user/cs20btech11000/Active",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
    )
    assert res.json()["status_code"] == 404


# Order Testing


def test_add_order():
    res = client.post(
        "/add-order",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        data=Order_Table(
            purchase_order_no="1",
            financial_year=2023,
            indentor="cs20btech11014",
        ).dict(),
        files=(),
    )
    assert res.status_code == 200

    res = client.post(
        "/add-order",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        data=Order_Table(
            purchase_order_no="2",
            financial_year=2023,
            indentor="cs20btech11015",
        ).dict(),
        files=(),
    )
    assert res.status_code == 200

    res = client.post(
        "/add-order",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        data=Order_Table(
            purchase_order_no="3",
            financial_year=2023,
            indentor="cs20btech11015",
        ).dict(),
        files=(),
    )
    assert res.status_code == 200

    # adding the existing order in table
    res = client.post(
        "/add-order",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        data=Order_Table(
            purchase_order_no="1",
            financial_year=2023,
            indentor="cs20btech11014",
        ).dict(),
        files=(),
    )

    assert res.status_code == 404

    # adding an order with non-existing indentor
    res = client.post(
        "/add-order",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        data=Order_Table(
            purchase_order_no="1",
            financial_year=2023,
            indentor="cs20btech110000",
        ).dict(),
        files=(),
    )

    assert res.status_code == 404


def test_update_order():
    res = client.put(
        "/update-order",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        data=Order_Table(
            purchase_order_no="1",
            financial_year=2023,
            indentor="cs20btech11014",
            invoice_no="1",
        ).dict(),
        files=(),
    )

    assert res.status_code == 200

    # updating a non-existing order
    res = client.put(
        "/update-order",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        data=Order_Table(
            purchase_order_no="56",
            financial_year=2023,
            indentor="cs20btech11014",
        ).dict(),
        files=(),
    )

    assert res.json()["status_code"] == 404

    # updating a order's indentor with non existing value
    res = client.put(
        "/update-order",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        data=Order_Table(
            purchase_order_no="1",
            financial_year=2023,
            indentor="cs20btech1101000",
        ).dict(),
        files=(),
    )

    assert res.status_code == 404


def test_delete_order():
    res = client.delete(
        "/delete-order/3/2023",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
    )

    assert res.status_code == 200

    # deleting non existing order
    res = client.delete(
        "/delete-order/67/2023",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
    )

    assert res.json()["status_code"] == 404


# Asset Testing


# Adding assets
def test_add_asset():
    res = client.post(
        "/add-asset",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        data=Asset(
            asset_name="Keyboard",
            model="DELL540",
            serial_no="154",
            asset_holder="cs20btech11014",
            purchase_order_no="1",
            financial_year=2023,
        ).dict(),
        files=(),
    )
    assert res.status_code == 200

    res = client.post(
        "/add-asset",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        data=Asset(
            asset_name="Mouse",
            model="HP M270",
            serial_no="1",
            asset_holder="cs20btech11014",
            purchase_order_no="1",
            financial_year=2023,
            entry_date="2023-05-2",
            warranty="2024-04-04",
        ).dict(),
        files=(),
    )
    assert res.status_code == 200

    # adding same serial number of the asset
    res = client.post(
        "/add-asset",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        data=Asset(
            asset_name="Mouse",
            model="HP M270",
            serial_no="1",
            asset_holder="cs20btech11015",
            purchase_order_no="1",
            financial_year=2023,
            entry_date="2023-05-2",
        ).dict(),
        files=(),
    )
    assert res.status_code == 404

    # giving wrong info of holder who is not the table
    res = client.post(
        "/add-asset",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        data=Asset(
            asset_name="Mouse",
            model="HP M270",
            serial_no="2",
            asset_holder="cs20btech11018",
            purchase_order_no="1",
            financial_year=2023,
            entry_date="2023-05-2",
            warranty="2024-04-04",
        ).dict(),
        files=(),
    )
    assert res.status_code == 404

    # wrong purchase order info
    res = client.post(
        "/add-asset",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        data=Asset(
            asset_name="Mouse",
            model="HP M270",
            serial_no="3",
            asset_holder="cs20btech11015",
            purchase_order_no="4",
            financial_year=2023,
            entry_date="2023-05-2",
            warranty="2024-04-04",
        ).dict(),
        files=(),
    )
    assert res.status_code == 404


def test_update_asset():
    res = client.put(
        "/update-asset",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        data=Asset(
            asset_name="Keyboard",
            model="DELL600",
            serial_no="1234",
            asset_holder="cs20btech11015",
            asset_location="C309",
        ).dict(),
        files=(),
    )
    assert res.status_code == 200

    # updating an asset not in the table
    res = client.put(
        "/update-asset",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        data=Asset(
            asset_name="Keyboard",
            model="DELL600",
            serial_no="25",
            asset_holder="cs20btech11015",
        ).dict(),
        files=(),
    )
    assert res.json()["status_code"] == 404

    # purchase order does not exist
    res = client.post(
        "/add-asset",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        data=Asset(
            asset_name="Mouse",
            model="HP M270",
            serial_no="3",
            asset_holder="cs20btech11015",
            purchase_order_no="4",
            financial_year=2023,
            entry_date="2023-05-2",
            warranty="2024-04-04",
        ).dict(),
        files=(),
    )
    assert res.status_code == 404


def test_delete_asset():
    res = client.delete(
        "/delete-asset/1234",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
    )
    assert res.status_code == 200

    # Deleteing an asset not in table
    res = client.delete(
        "/delete-asset/5486",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
    )
    assert res.json()["status_code"] == 404


# Bulk Asset Testing


def test_add_bulk_asset():
    res = client.post(
        "/add-bulk-asset",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        data=Bulk_Asset(
            asset_name="chair",
            model="godrej",
            serial_no="1",
            asset_location="ALH2",
            purchase_order_no="2",
            financial_year=2023,
            # picture=None,
        ).dict(),
        files=(),
    )
    assert res.status_code == 200

    # adding same serial number of the asset
    res = client.post(
        "/add-bulk-asset",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        data=Bulk_Asset(
            asset_name="table",
            model=None,
            serial_no="1",
            asset_location="ALH2",
            purchase_order_no="173",
            financial_year=2023,
            entry_date="2023-05-2",
            warranty="2024-04-04",
        ).dict(),
        files=(),
    )
    assert res.status_code == 404

    # purchase order does not exist
    res = client.post(
        "/add-bulk-asset",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        data=Bulk_Asset(
            asset_name="table",
            serial_no="3",
            asset_location="lab",
            purchase_order_no="4",
            financial_year=2023,
            entry_date="2023-05-2",
        ).dict(),
        files=(),
    )
    assert res.status_code == 404


def test_update_bulk_asset():
    res = client.put(
        "/update-bulk-asset",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        data=Bulk_Asset(
            asset_name="chair",
            model="LG",
            serial_no="1",
            # picture=None,
        ).dict(),
        files=(),
    )
    assert res.status_code == 200

    # updating an non existing asset
    res = client.put(
        "/update-bulk-asset",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        data=Bulk_Asset(
            asset_name="chair",
            model="LG",
            serial_no="10",
            # picture=None,
        ).dict(),
        files=(),
    )
    assert res.json()["status_code"] == 404

    # purchase order does not exists
    res = client.put(
        "/update-bulk-asset",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        data=Bulk_Asset(
            asset_name="chair",
            model="LG",
            serial_no="1",
            purchase_order_no="147850",
            financial_year=2023,
            # picture=None,
        ).dict(),
        files=(),
    )
    assert res.status_code == 404


def test_delete_bulk_asset():
    res = client.delete(
        "/delete-bulk-asset/1/ALH2",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
    )
    assert res.status_code == 200

    # Deleting non existing asset
    res = client.delete(
        "/delete-bulk-asset/20/lab",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
    )
    assert res.json()["status_code"] == 404
