from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.config.config import settings

database_url = f'postgresql+psycopg2://' \
               f'{settings.DB_USERNAME}:{settings.DB_PASSWORD}' \
               f'@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'

engine = create_engine(database_url, echo=True, future=True)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    with Session(engine) as session:
        yield session
