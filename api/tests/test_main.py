from fastapi.testclient import TestClient
from main import app
from utils.auth import get_user_details, override_get_user_details
import pytest

from models.db import User, Asset, Bulk_Asset, Order_Table


client = TestClient(app)


if __name__ == "__main__":
    app.dependency_overrides[get_user_details] = override_get_user_details
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
    # assert res.json() == {"detail": "user added"}

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
    # assert res.json() == {"detail": "user added"}

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
    # assert res.json() == {"detail": "user added"}
    
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
    assert res.status_code == 400
    # assert res.json() == {"detail": "Cant add user"}

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
    # assert res.json() == {"detail": "Cant add user"}
    
    #same user_id and same email_id as student
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
    # assert res.json() == {"detail": "user added"}
    
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
    assert res.status_code == 400
    # assert res.json() == {"detail": "cant add user"}


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
        "/activate-deactivate-user/cs20btech11024/Inactive",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
    )
    assert res.status_code == 200
    assert res.json() == {"detail": "user state changed"}
    
    res = client.put(
        "/activate-deactivate-user/cs20btech11024/Active",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
    )
    assert res.status_code == 200
    assert res.json() == {"detail": "user state unchanged"}
    
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
    assert res.status_code == 200
    print(res.json)
    
    res = client.post(
        "/get-user",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        json=User(user_type="Faculty", department="CSE").dict(),
    )
    assert res.status_code == 200
    print(res.json)
    


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
    
    res = client.post(
        "/add-order",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        json=Order_Table(
            purchase_order_no="1",
            financial_year=2023,
            indentor="cs20btech11014",
            total_price=2500,
            invoice_date='2023-05-2',
        ).dict(),
        files=(),
    )

    assert res.status_code == 200
    # assert res.json() == {"detail": "asset added"}
    print(res.json())
    
    #adding the existing iteam in table
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

    assert res.status_code == 400
    #assert res.json()=={"detail":"asset already added"}
    print(res.json)


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

    res = client.post(
        "/add-asset",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        data=Asset(
            asset_name="Mouse",
            model="HP M270",
            serial_no="173",
            asset_holder="cs20btech11014",
            purchase_order_no="1",
            financial_year=2023,
            entry_date='2023-05-2',
            Warranty='2024-04-04',
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

    res = client.post(
        "/get-asset",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        json=Asset(
            asset_name="Mousepad",
        ).dict(),
    )
    data = res.json()
    assert res.status_code == 200
    print(data)
    # assert res.json() == {"detail": "asset not found"}


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

    res = client.post(
        "/add-bulk-asset",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        data=Bulk_Asset(
            asset_name="Dining-Table",
            serial_no="456",
            purchase_order_no="1",
            financial_year=2023,
            deparment="CSE",
            quantity=1,
            entry_date='2023-05-02',
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

    res = client.post(
        "/get-bulk-asset",
        headers={"Authorization": "cs20btech11024@iith.ac.in"},
        json=Bulk_Asset(
            asset_name="Sofa",
        ).dict(),
    )
    data = res.json()
    assert res.status_code == 200
    print(data)
    # assert res.json() == {"detail": "Bulk asset not found"}
