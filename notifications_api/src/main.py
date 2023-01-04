import uvicorn as uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.v1 import user

app = FastAPI(
    title="API for sending email-notifications",
    docs_url="/notify/openapi",
    openapi_url="/notify/openapi.json",
    description="",
    # default_response_class=ORJSONResponse,
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
    user.router, prefix='/api/v1/users',
    tags=['users']
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
    )
# uvicorn src.main:app --host=0.0.0.0 --reload
# http://localhost:8000/notify/openapi