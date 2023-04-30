from pydantic import BaseModel, EmailStr
from typing import List
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
import asyncio
from utils.configs import Config


conf = ConnectionConfig(
    MAIL_USERNAME=Config.MAIL_USERNAME,
    MAIL_PASSWORD=Config.MAIL_PASSWORD,
    MAIL_FROM=Config.MAIL_FROM,
    MAIL_PORT=Config.MAIL_PORT,
    MAIL_SERVER=Config.MAIL_SERVER,
    MAIL_STARTTLS=Config.MAIL_STARTTLS,
    MAIL_SSL_TLS=Config.MAIL_SSL_TLS,
    USE_CREDENTIALS=Config.MAIL_USE_CREDENTIALS,
    VALIDATE_CERTS=Config.MAIL_VALIDATE_CERTS,
)
override_conf = None


class EmailSchema(BaseModel):
    email: List[EmailStr]


email = EmailSchema(email=["cs20btech11014@iith.ac.in"])


async def send_email(subject: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=email.dict().get("email"),
        body=body,
        subtype=MessageType.html,
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    return


def send_email_(subject: str, body: str):
    asyncio.run(send_email(subject, body))
    return


def override_send_email_(subject: str, body: str):
    print("mail from overrride mail...")
    return
