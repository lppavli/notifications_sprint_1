import json

from fastapi import APIRouter, Query
from starlette.responses import JSONResponse

from starlette.templating import Jinja2Templates

from admin.services import producer

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post('/', description='Create new mailing',
             response_description='Mailing created',
             )
async def create_mailing(
        title: str,
        text: str,
        emails: list[str] = Query(default=[]),  # type: ignore
):
    """Send letters to users."""
    notice = {'title': title,
              'text': text,
              'emails': emails}
    await producer.send_msg(notice=json.dumps(notice, default=str))
    return JSONResponse(status_code=200, content={"message": "emails have been sent"})
