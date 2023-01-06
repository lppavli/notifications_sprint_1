import json
from datetime import datetime

import jwt
from sqlalchemy import update

from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette import status

from starlette.responses import JSONResponse, HTMLResponse
from starlette.templating import Jinja2Templates

from src.db.db import async_session
from src.models.events import Source, EventType, Notice
from src.models.user import User
from src.services import producer
from src.services.auth import Auth
from worker.auth_data import get_data_from_auth

router = APIRouter()
templates = Jinja2Templates(directory="templates")
security = HTTPBearer()
auth_handler = Auth()


@router.post('/signup', description='New user',
             response_description='User registration',
             )
async def user_registration(
        credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Send welcome letter to user."""
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)
    source = Source.email
    event_type = EventType.welcome_letter
    notice = Notice(
        user_id=user_id,
        source=source,
        event_type=event_type,
        scheduled_datetime=datetime.now()
    )
    await producer.send_msg(notice=json.dumps(notice.dict(), default=str))
    return JSONResponse(status_code=200, content={"message": "email has been sent"})


@router.get('/verification', response_class=HTMLResponse)
async def email_verification(request: Request, token: str):
    async with async_session() as session:
        async with session.begin():
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            user = get_data_from_auth(payload["id"])
            query = update(User).where(id == str(payload["id"]))
            query = query.values(is_verified=True)
            query.execution_options(synchronize_session="fetch")
            await session.execute(query)
            if user:
                return templates.TemplateResponse("verification.html",
                                                  {"request": request,
                                                   "username": f'{user["first_name"]} {user["last_name"]}'})
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
