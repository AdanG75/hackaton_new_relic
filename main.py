from typing import Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from starlette.responses import JSONResponse

from db import mongo_connection
from routes import incendios_router, lugares_router, usuario_router
from schemas.schemas import BasicResponse

app = FastAPI(title="Backend Hackaton", version="0.1.0")

app.include_router(router=incendios_router.router)
app.include_router(router=lugares_router.router)
app.include_router(router=usuario_router.router)

origins = [
        'http://0.0.0.0/0:4200'
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=BasicResponse,
    response_class=JSONResponse,
    tags=['Main']
)
async def print_hi(
        name: Optional[str] = Query(None, max_length=80)
):
    msg = "Hello World" if name is None else f"Hello {name}"

    return BasicResponse(response=msg)


@app.get(
    path="/test-mongo",
    tags=['Test']
)
async def test_mongo():
    msg = mongo_connection.ping_mongo()
    return BasicResponse(response=msg)
