import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from pathlib import Path
from config_section.config import config


class EmailService:
    def __init__(self):
        mail_config = config.MAIL_CONFIG
        self.ses = boto3.client(
            "ses",
            region_name=mail_config.mail_region,
            aws_access_key_id=mail_config.mail_username,
            aws_secret_access_key=mail_config.mail_password,
        )
        self.sender_email = mail_config.mail_sender

    def send_email(self, to_email: str, subject: str, message: str):
        try:
            response = self.ses.send_email(
                Source=self.sender_email,
                Destination={"ToAddresses": [to_email]},
                Message={
                    "Subject": {"Data": subject},
                    "Body": {"Text": {"Data": message}},
                },
            )
            print(response["MessageId"])
            return response["MessageId"]
        except ClientError as e:
            raise Exception(f"Email sending failed: {str(e)}")


EmailService().send_email(to_email="martin422420@gmail.com", subject="this is test mail", message="hello from test mail :)")