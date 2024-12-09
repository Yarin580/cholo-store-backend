
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from config_section.config import config

mail_config = config.MAIL_CONFIG
print(mail_config.mail_from)
conf = ConnectionConfig(
    MAIL_USERNAME=mail_config.mail_username,
    MAIL_PASSWORD=mail_config.mail_password,
    MAIL_FROM=mail_config.mail_from,
    MAIL_PORT=mail_config.mail_port,
    MAIL_SERVER=mail_config.mail_server,
    MAIL_SSL_TLS=mail_config.mail_ssl,
    MAIL_STARTTLS=mail_config.mail_tls
)
