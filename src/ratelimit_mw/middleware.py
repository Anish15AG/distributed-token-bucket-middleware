from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

class RateLimitMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, redis_url: str = "redis://localhost:6379/0"):
        super().__init__(app)
        self.redis_url = redis_url
        # TODO: Initialize Redis client connection here
    
    async def dispatch(self, request, call_next) -> Response:
        response = await call_next(request)
        return response