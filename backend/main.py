import fastapi
from aioredis import Redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.util import greenlet_spawn
from starlette.middleware.base import BaseHTTPMiddleware

from middlewares.html_page import html_page_middleware
from middlewares.response_validation import response_validation_middleware, parse_raw
from middlewares.server_timing import ServerTimingMiddleware
from root_router import root_router

app = FastAPI()
app.include_router(root_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origin_regex=r'https?://localhost:[0-9]{1,5}',
    allow_methods=['*'],
    allow_headers=['*'],
)

app.add_middleware(
    BaseHTTPMiddleware,
    dispatch=response_validation_middleware
)

app.add_middleware(
    BaseHTTPMiddleware,
    dispatch=html_page_middleware
)

app.add_middleware(ServerTimingMiddleware, calls_to_track={
    'dependencies_execution': (fastapi.routing.solve_dependencies,),
    'endpoint_running': (fastapi.routing.run_endpoint_function,),
    'pydantic_validation': (fastapi.routing.serialize_response,),
    'pydantic_validation_': (parse_raw,),
    'json_rendering': (
        fastapi.responses.JSONResponse.render,
        fastapi.responses.ORJSONResponse.render,
    ),
    'sql_requests': (greenlet_spawn,),
    'redis_requests': (Redis.execute_command,),
    'total': (response_validation_middleware,)
})
