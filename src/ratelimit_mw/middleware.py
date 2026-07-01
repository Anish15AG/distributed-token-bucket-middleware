import time
import redis.asyncio as aioredis
from redis.exceptions import WatchError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from .config import RateLimitConfig


class RateLimitMiddleware(BaseHTTPMiddleware):

    # ASGI middleware implementation of Token Bucket Algorithm
    def __init__(self, app, config: RateLimitConfig = None):
        super().__init__(app)
        self.config = config or RateLimitConfig()

        self.redis = aioredis.from_url(
            self.config.redis_url,
            decode_responses=True
        )

    async def dispatch(self, request: Request, call_next) -> Response:
        identity = self.config.key_resolver(request)
        bucket_key = f"ratelimit:{identity}"

        cost = self.config.cost_resolver(request)

        # Check and consume tokens
        allowed, remaining, retry_after = await self._process_bucket(bucket_key, cost)

        if not allowed:
            return JSONResponse(
                status_code=429,
                content={"error": "Rate Limit exceeded. Please try again later"},
                headers={"Retry-After": str(int(retry_after) + 1)},
            )


        response = await call_next(request)

        response.headers["X-RateLimit-Limit"] = str(self.config.capacity)
        response.headers["X-RateLimit-Remaining"] = str(int(remaining))

        # Calculation of Bucket refill time
        tokens_needed_to_full = self.config.capacity - remaining
        seconds_to_full = tokens_needed_to_full / self.config.refill_rate
        reset_timestamp = int(time.time() + seconds_to_full)

        response.headers["X-RateLimit-Reset"] = str(reset_timestamp)
        
        return response

    async def _process_bucket(self, bucket_key: str, cost: int):
        capacity = self.config.capacity
        refill_rate = self.config.refill_rate

        while True:
            try:

                async with self.redis.pipeline() as pipe:
                    
                    await pipe.watch(bucket_key)
                    

                    bucket_state = await pipe.hgetall(bucket_key)
                    
                    now = time.time()

                    if not bucket_state:
                        current_tokens = float(capacity)
                        last_refill = now
                    else:
                        stored_tokens = float(bucket_state.get("tokens", 0))
                        last_refill = float(bucket_state.get("last_refill", now))
                        time_passed = now - last_refill
                        tokens_to_add = time_passed * refill_rate
                        current_tokens = min(capacity, stored_tokens + tokens_to_add)

                    # Check if user has enough tokens
                    if current_tokens < cost:
                        tokens_needed = cost - current_tokens
                        retry_after = tokens_needed / refill_rate
                        
                        await pipe.unwatch()
                        
                        return False, current_tokens, retry_after

                    # Consume token
                    current_tokens -= cost

                    # Start the transaction block
                    pipe.multi()
                    
                    # Queue the updates
                    pipe.hset(bucket_key, mapping={
                        "tokens": str(current_tokens),
                        "last_refill": str(now)
                    })
                    pipe.expire(bucket_key, 60)
                    
                    # Execute the transaction block
                    await pipe.execute()

                    return True, current_tokens, 0

            except WatchError:

                continue