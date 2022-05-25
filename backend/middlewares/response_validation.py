from typing import Any, Sequence, Type

from fastapi import Request
from fastapi.responses import ORJSONResponse
from fastapi.routing import APIRouter
from pydantic import BaseModel
from pydantic.main import ModelMetaclass
from starlette.responses import StreamingResponse
from starlette.routing import Match


def parse_raw(model: Type[BaseModel], content: str | bytes):
    """Wrapper over pydantic.BaseModel.parse_raw method.

    Created to measure execution time of this method inside response_validation_middleware.
    Measured with ServerTimingMiddleware, result passes to the header 'server-timing' in all server responses.

    """
    return model.parse_raw(content)


class AsyncGenerator:
    """Returns async version of generator based on passed sequence."""

    def __init__(self, items: Sequence[Any]):
        self.items = items
        self.iterator = items.__iter__()

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return self.iterator.__next__()
        except:
            raise StopAsyncIteration


async def response_validation_middleware(request: Request, call_next):
    """Validates server response using pydantic models.

    Issue: fastapi.routing.serialize_response, which fastapi uses to validate endpoint responses,
    is too slow (10 kb validates ~300-400 ms).
    Solution: Return ORJSONResponse. In this case fastapi does not validate response.
    That middleware does this.
    It extracts response_model from response and validates response just calling .parse_raw().
    At 160 kb size speedup reaches 10 times (~30 ms).

    Additionally: by measuring execution time of this function, ServerTimingMiddleware calculates
    total server response time and passes it to the 'server-timing' header.

    """
    response: StreamingResponse = await call_next(request)
    response_body = [x async for x in response.body_iterator]  # Ответ представлен в виде async-генератора
    response.body_iterator = AsyncGenerator(response_body)  # Проитерировав исходный генератор, подставляем непроитерированную копию

    router: APIRouter = request.scope['router']
    for route in router.routes:
        match, _ = route.matches(request.scope)
        if match == Match.FULL:
            if hasattr(route, 'response_class') \
                    and route.response_class is ORJSONResponse \
                    and response.status_code == 200 \
                    and hasattr(route, 'response_model') \
                    and issubclass(route.response_model.__class__, ModelMetaclass):
                parse_raw(route.response_model, response_body[0])
            break

    return response
