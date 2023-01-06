from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class UserModel(BaseModel):
    id: str
    login: str
    email: str
    first_name: str
    last_name: str


class Source(str, Enum):
    email = 'email'
    sms = 'sms'
    push = 'push'


class EventType(str, Enum):
    welcome_letter = 'welcome_letter'
    critique_likes = 'critique_likes'


class Notice(BaseModel):
    user_id: str
    source: Source
    event_type: EventType
    scheduled_datetime: datetime
