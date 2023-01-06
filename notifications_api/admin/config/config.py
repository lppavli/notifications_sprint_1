from typing import Optional

from fastapi_mail import ConnectionConfig
from pydantic import BaseSettings


class Settings(BaseSettings):
    # Postgres
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: str

    # Rabbit
    RABBITMQ_USER: str
    RABBITMQ_PASS: str

    RABBITMQ_EXCHANGE: Optional[str]
    RABBITMQ_EXCHANGE_TYPE: Optional[str]
    RABBITMQ_QUEUE_NAME: Optional[str]

    RABBITMQ_HOST: Optional[str]
    RABBITMQ_PORT: Optional[str]

    # Mail
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str

    AUTH_SERVICE: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'


settings = Settings()

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER='templates',
)
