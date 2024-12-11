import os
from dotenv import load_dotenv

load_dotenv()

class AWSCredentials:
    aws_access_key_id: str = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str = os.getenv("AWS_SECRET_ACCESS_KEY")

class JwtConfig:
    secret_key: str = os.getenv("JWT_SECRET_KEY")
    algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    expires_in: int = os.getenv("JWT_EXPIRES_IN", 30)

class MailConfig:
    mail_password: str = os.getenv("MAIL_PASSWORD")
    mail_username: str = os.getenv("MAIL_USERNAME")
    mail_sender: str = os.getenv("MAIL_SENDER")
    mail_region: str = os.getenv("MAIL_REGION")

class Config:
    ENV: str = "development"
    DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    JWT_SECRET_KEY: str = "fastapi"
    JWT_ALGORITHM: str = "HS256"
    DB_URL: str = os.getenv("DB_URL")
    AWS_CREDS: AWSCredentials = AWSCredentials()
    JWT_CONFIG: JwtConfig = JwtConfig()
    MAIL_CONFIG: MailConfig = MailConfig()


class DevelopmentConfig(Config):
    pass

class LocalConfig(Config):
    pass


class ProductionConfig(Config):
    ENV: str = "production"
    DEBUG: str = False
    pass


def get_config() -> Config:
    load_dotenv()
    env = os.getenv("ENV", "LOCAL")
    config_type = {
        "DEV": DevelopmentConfig(),
        "LOCAL": LocalConfig(),
        "PROD": ProductionConfig(),
    }
    return config_type[env]


config = get_config()
