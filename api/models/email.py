from pydantic import BaseModel, EmailStr
from typing import List
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType


conf = ConnectionConfig(
    MAIL_USERNAME="cs20btech11015@iith.ac.in",
    MAIL_PASSWORD="dofsrmwuzukfxure",
    MAIL_FROM="cs20btech11015@iith.ac.in",
    MAIL_PORT=465,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


class EmailSchema(BaseModel):
    email: List[EmailStr]


email = EmailSchema(email=["cs20btech11015@iith.ac.in"])
