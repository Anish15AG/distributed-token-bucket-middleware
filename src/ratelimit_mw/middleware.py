import asyncio
import time
import httpx
import redis.asyncio as aioredis
from redis.exceptions import WatchError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from .config import RateLimitConfig


class RateLimitMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, config: RateLimitConfig = None):
        super().__init__(app)
        self.config = config or RateLimitConfig()
        self.redis = aioredis.from_url(
            self.config.redis_url,
            decode_responses=True
        )

        self.current_load_factor = 1.0
        self.active_requests = 0
        self._tasks_started = False

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http" and not self._tasks_started:
            self._tasks_started = True
            asyncio.create_task(self._run_health_monitor())

        await super().__call__(scope, receive, send)

    async def _run_health_monitor(self):
        if self.config.health_check_url:
            await self._http_health_poller()
        else:
            await self._local_health_monitor()
    
    async def _http_health_poller(self):
        async with httpx.AsyncClient(timeout=2.0) as client:
            while True:
                try:
                    resp = await client.get(self.config.health_check_url)
                    if resp.status_code == 200:
                        data = resp.json()
                        self.current_load_factor = float(data.get("load_factor", 1.0))
                    
                except Exception:
                    self.current_load_factor = 1.0
                
                await asyncio.sleep(self.config.health_check_interval)

    
    async def _local_health_monitor(self):
        while True:
            self.current_load_factor = float(self.active_requests)
            await asyncio.sleep(1.0) 

    async def dispatch(self, request: Request, call_next) -> Response:

        if self.current_load_factor > self.config.max_load_factor:
            return JSONResponse(
                status_code=503,
                content={"error":"Service temporarily unavailable due to high demand"},
                headers={"Retry-After":"5"}
            )
        
        self.active_requests+=1
        try:
            identity = self.config.key_resolver(request)
            org_id = self.config.org_resolver(request)
            cost = self.config.cost_resolver(request)

            key_bucket = f"ratelimit:key:{identity}"
            org_bucket = f"ratelimit:org:{org_id}"

            allowed, remaining, retry_after = await self._process_nested_buckets(
            key_bucket, org_bucket, cost
            )

            if not allowed:
                return JSONResponse(
                    status_code=429,
                    content={"error": "Rate limit exceeded. Please try again later."},
                    headers={"Retry-After": str(int(retry_after) + 1)},
                )

            response = await call_next(request)
            response.headers["X-RateLimit-Limit"] = str(self.config.capacity)
            response.headers["X-RateLimit-Remaining"] = str(int(remaining))
            response.headers["X-RateLimit-LoadFactor"] = str(self.current_load_factor)
            return response
        
        finally:
            self.active_requests -= 1

    async def _process_nested_buckets(self, key_bucket: str, org_bucket: str, cost: int):
        capacity = self.config.capacity
        refill_rate = self.config.refill_rate
        org_capacity = capacity * 5

        while True:
            try:
                async with self.redis.pipeline(transaction=True) as pipe:
                    await pipe.watch(key_bucket, org_bucket)

                    key_state = await pipe.hgetall(key_bucket)
                    org_state = await pipe.hgetall(org_bucket)
                    now = time.time()

                    if not key_state:
                        key_tokens = float(capacity)
                    else:
                        stored = float(key_state.get("tokens", capacity))
                        last = float(key_state.get("last_refill", now))
                        key_tokens = min(capacity, stored + (now - last) * refill_rate)

                    if not org_state:
                        org_tokens = float(org_capacity)
                    else:
                        stored = float(org_state.get("tokens", org_capacity))
                        last = float(org_state.get("last_refill", now))
                        org_tokens = min(org_capacity, stored + (now - last) * refill_rate)

                    if key_tokens < cost or org_tokens < cost:
                        await pipe.unwatch()
                        min_tokens = min(key_tokens, org_tokens)
                        tokens_needed = cost - min_tokens
                        retry_after = tokens_needed / refill_rate
                        return False, min(key_tokens, org_tokens), retry_after

                    key_tokens -= cost
                    org_tokens -= cost

                    pipe.multi()

                    pipe.hset(key_bucket, mapping={
                        "tokens": str(key_tokens),
                        "last_refill": str(now)
                    })
                    pipe.expire(key_bucket, 3600)

                    pipe.hset(org_bucket, mapping={
                        "tokens": str(org_tokens),
                        "last_refill": str(now)
                    })
                    pipe.expire(org_bucket, 3600)

                    await pipe.execute()

                    return True, key_tokens, 0

            except WatchError:
                continue