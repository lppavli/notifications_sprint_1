import uvicorn as uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from admin.api.v1 import mailing

app = FastAPI(
    title="API for sending emails for admin",
    docs_url="/admin/openapi",
    openapi_url="/admim/openapi.json",
    description="",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


app.include_router(
    mailing.router, prefix='/api/v1/mailing',
    tags=['create mail']
)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8002,
    )
# uvicorn admin.main:app --host=0.0.0.0 --reload
# http://localhost:8000/admin/openapi