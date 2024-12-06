import os
from dotenv import load_dotenv

class AWSCredentials:
    aws_access_key_id: str = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str = os.getenv("AWS_SECRET_ACCESS_KEY")

class JwtConfig:
    secret_key: str = os.getenv("JWT_SECRET_KEY")
    algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    expires_in: int = os.getenv("JWT_EXPIRES_IN", 30)

class Config:
    ENV: str = "development"
    DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    DB_URL: str = f"mysql+aiomysql://fastapi:fastapi@localhost:3306/fastapi"
    JWT_SECRET_KEY: str = "fastapi"
    JWT_ALGORITHM: str = "HS256"
    AWS_CREDS: AWSCredentials = AWSCredentials()
    JWT_CONFIG: JwtConfig = JwtConfig()


class DevelopmentConfig(Config):
    DB_URL: str = f"mysql+aiomysql://root:fastapi@db:3306/fastapi"

class LocalConfig(Config):
    DB_URL: str = f"postgresql://postgres:password@localhost/cholo-store"


class ProductionConfig(Config):
    DEBUG: str = False
    DB_URL: str = f"mysql+aiomysql://fastapi:fastapi@localhost:3306/prod"


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
