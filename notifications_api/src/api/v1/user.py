import json
from datetime import datetime

import jwt
from fastapi import APIRouter, Request, HTTPException
from starlette import status

from starlette.responses import JSONResponse, HTMLResponse
from starlette.templating import Jinja2Templates

from src.db.db import session
from src.models.events import UserModel, Source, EventType, Notice
from src.models.user import User
from src.services import producer

router = APIRouter()
templates = Jinja2Templates(directory="templates")
session = session()


@router.post('/signup', description='New user',
             response_description='User registration',
             )
async def user_registration(
        login: str,
        email: str,
        password: str,
        first_name: str,
        last_name: str
):
    """Send welcome letter to user."""
    new_user = User(login=login, email=email, first_name=first_name, last_name=last_name)
    new_user.set_password(password)
    session.add(new_user)
    session.commit()
    print(new_user)
    user = UserModel(id=str(new_user.id),
                     login=new_user.login,
                     email=new_user.email,
                     first_name=first_name,
                     last_name=last_name
                     )
    source = Source.email
    event_type = EventType.welcome_letter
    notice = Notice(
        user=user,
        source=source,
        event_type=event_type,
        scheduled_datetime=datetime.now()
    )
    await producer.send_msg(notice=json.dumps(notice.dict(), default=str))
    return JSONResponse(status_code=200, content={"message": "email has been sent"})


@router.get('/verification', response_class=HTMLResponse)
async def email_verification(request: Request, token: str):
    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    # payload = jwt.decode(token, config_credentials['SECRET'])
    user = session.query(User).filter(User.id == payload["id"]).first()
    session.query(User).filter(User.id == payload['id']).update(
        {"is_verified": True}, synchronize_session="fetch")
    session.commit()
    if user:
        print('&&&&&&')
        return templates.TemplateResponse("verification.html",
                                          {"request": request,
                                           # })
                                           "username": f"{user.first_name} {user.last_name}"})
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
