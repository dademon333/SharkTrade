import re

from fastapi import Response

from config import Config


_COMPILED_ORIGIN_REGEX = re.compile(Config.CORS_ALLOWED_ORIGINS_REGEX)


async def cors_handler(request, exception):  # noqa
    """Adds cors policies to response on internal server error.

    Added because default fastapi CORSMiddleware ignore this case.
    Code original: https://github.com/tiangolo/fastapi/issues/775#issuecomment-723628299
    """
    response = Response(content='Internal Server Error', status_code=500)

    origin = request.headers.get('origin')
    if origin:
        response.headers["Access-Control-Allow-Credentials"] = 'true'
        if _COMPILED_ORIGIN_REGEX.fullmatch(origin):
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers.add_vary_header("Origin")

    return response
