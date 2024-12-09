import asyncio

from fastapi_mail import FastMail, MessageSchema
from fastapi import BackgroundTasks
from pydantic import EmailStr
from src.modules.mailer.setup import conf


async def send_email(subject: str, email_to: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],  # List of recipients
        body=body,
        subtype="plain"  # Use "plain" for plain text emails
    )

    fm = FastMail(conf)
    await fm.send_message(message)



asyncio.run(send_email(subject="Hello World!", email_to="hershyarin@gmail.com", body="Hello World!"))