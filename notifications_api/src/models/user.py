import uuid as uuid
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import declarative_base

CommonBase = declarative_base()


def new_uuid() -> uuid.UUID:
    val = uuid.uuid4()
    while val.hex[0] == "0":
        val = uuid.uuid4()
    return str(val)


class User(CommonBase):
    __tablename__ = 'users'
    id = Column(String, primary_key=id, default=new_uuid, unique=True, nullable=False)
    login = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    password = Column(String, nullable=False)
    is_superuser = Column(Boolean, default=False)
    email = Column(String, unique=True, nullable=False)
    is_verified = Column(Boolean, default=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)
        return self

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_email_verified(self):
        self.is_verified = True
        return self
