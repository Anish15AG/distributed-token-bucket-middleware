import time
import redis.asyncio as aioredis
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

    # FIX 1: Un-indented so it is a class method, not a nested function
    async def dispatch(self, request: Request, call_next) -> Response:
        identity = request.client.host if request.client else "unknown"
        
        # FIX 5: Removed spaces in the key name for clean Redis keys
        bucket_key = f"ratelimit:{identity}"

        # Current bucket state from Redis
        bucket_state = await self.redis.hgetall(bucket_key)

        now = time.time()
        capacity = self.config.capacity
        refill_rate = self.config.refill_rate
        cost = 1 # Every request costs 1 token

        if not bucket_state:
            # First time user: Initialize the bucket and consume a token
            current_tokens = float(capacity - cost)
            last_refill = now
        else:
            # Returning user: Applying lazy refill calculation
            stored_tokens = float(bucket_state.get("tokens", 0))
            last_refill = float(bucket_state.get("last_refill", now))

            # Calculation: how many tokens to be added since past request
            time_passed = now - last_refill
            tokens_to_add = time_passed * refill_rate

            # Add tokens operation (should avoid exceeding limit of bucket)
            current_tokens = min(capacity, stored_tokens + tokens_to_add)

            # User does NOT have enough tokens
            if current_tokens < cost:
                tokens_needed = cost - current_tokens
                retry_after_seconds = tokens_needed / refill_rate

                # Block Request
                return JSONResponse(
                    status_code=429,
                    content={"error": "Rate Limit exceeded. Please try again later"},
                    headers={"Retry-After": str(int(retry_after_seconds) + 1)},
                )
            
            # Consume token once request processed
            current_tokens -= cost

        # Store the new updated state to Redis
        await self.redis.hset(bucket_key, mapping={
            "tokens": str(current_tokens),
            "last_refill": str(now) 
        })

        await self.redis.expire(bucket_key, 60)

        response = await call_next(request)

        # Rate limit headers
        response.headers["X-RateLimit-Limit"] = str(capacity)
        response.headers["X-RateLimit-Remaining"] = str(int(current_tokens))

        return response