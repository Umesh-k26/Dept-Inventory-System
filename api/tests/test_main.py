from fastapi.testclient import TestClient
from main import app
from utils.auth import get_email, override_get_email
import pytest

from models.db import User, Asset, Bulk_Asset, Order_Table


client = TestClient(app)


if __name__ == "__main__":
    app.dependency_overrides[get_email] = override_get_email
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
    assert res.json() == {"detail": "user added"}

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
    assert res.json() == {"detail": "user added"}

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
    assert res.json() == {"detail": "user added"}

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
    assert res.status_code == 400
    assert res.json() == {"detail": "Cant add user"}

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
    assert res.status_code == 400
    assert res.json() == {"detail": "Cant add user"}


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
    assert res.json() == {"detail": "User Updated"}

    # updating email to already existing email
    res = client.put(
        "/update-user",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        json=User(
            user_id="cs20btech11015",
            email="cs20btech11014@iith.ac.in",
        ).dict(),
    )
    assert res.status_code == 400
    assert res.json() == {"detail": "Cant update user"}


def test_activate_deactivate_user():
    res = client.put(
        "/activate-deactivate-user/cs20btech11014/Inactive",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
    )
    assert res.status_code == 200
    assert res.json() == {"detail": "user state changed"}

    res = client.put(
        "/activate-deactivate-user/cs20btech11000/Active",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
    )
    assert res.status_code == 201
    assert res.json() == {"detail": "User not found"}


def test_filter_users():
    res = client.post(
        "/get-user",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        json=User(user_type="Stud", department="CSE").dict(),
    )
    data = res.json()
    assert res.status_code == 200
    for user in data:
        print(user)


# Order Testing


def test_add_order():
    res = client.post(
        "/add-order",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        json=Order_Table(
            purchase_order_no="1",
            financial_year=2023,
            indentor="cs20btech11014",
        ).dict(),
        files=(),
    )

    assert res.status_code == 200
    # assert res.json() == {"detail": "asset added"}
    print(res.json())


# Asset Testing


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
            # picture=None,
        ).dict(),
        files=(),
    )

    assert res.status_code == 200
    # assert res.json() == {"detail": "asset added"}
    print(res.json())


def test_update_asset():
    res = client.put(
        "/update-asset",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        data=Asset(
            asset_name="Keyboard",
            model="DELL600",
            serial_no="1234",
            asset_holder="cs20btech11015",
            # picture=None,
        ).dict(),
        files=(),
    )

    assert res.status_code == 200
    # assert res.json() == {"detail": "asset added"}
    print(res.json())


def test_filter_asset():
    res = client.post(
        "/get-asset",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        json=Asset(
            asset_name="Keyboard",
        ).dict(),
    )
    data = res.json()
    assert res.status_code == 200
    for asset in data:
        print(asset)


# Bulk Asset Testing


def test_add_bulk_asset():
    res = client.post(
        "/add-bulk-asset",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        data=Bulk_Asset(
            asset_name="Keyboard",
            model="DELL540",
            serial_no="154",
            purchase_order_no="1",
            financial_year=2023,
            # picture=None,
        ).dict(),
        files=(),
    )

    assert res.status_code == 200
    # assert res.json() == {"detail": "asset added"}
    print(res.json())


def test_update_bulk_asset():
    res = client.put(
        "/update-bulk-asset",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        data=Bulk_Asset(
            asset_name="Keyboard",
            model="DELL600",
            serial_no="1234",
            # picture=None,
        ).dict(),
        files=(),
    )

    assert res.status_code == 200
    # assert res.json() == {"detail": "asset added"}
    print(res.json())


def test_filter_bulk_asset():
    res = client.post(
        "/get-bulk-asset",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        json=Bulk_Asset(
            asset_name="Table",
        ).dict(),
    )
    data = res.json()
    assert res.status_code == 200
    for asset in data:
        print(asset)
