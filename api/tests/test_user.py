from test_main import client
from models.db import User


def test_add_user(client):
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