import asyncio
import pytest
import httpx
import redis.asyncio as aioredis
from collections import Counter
from fastapi import FastAPI
from ratelimit_mw import RateLimitMiddleware
from ratelimit_mw.config import RateLimitConfig

@pytest.fixture(autouse=True)
async def clean_redis():
    client = aioredis.from_url("redis://localhost:6379/1", decode_responses=True)
    await client.flushdb()
    yield
    await client.flushdb()
    await client.aclose()

@pytest.fixture
def app():
    application = FastAPI()
    
    @application.get("/ping")
    async def ping():
        return {"msg": "pong"}
    
    config = RateLimitConfig(
        capacity=10, 
        refill_rate=0.1,
        redis_url="redis://localhost:6379/1"
    )
    application.add_middleware(RateLimitMiddleware, config=config)
    return application

@pytest.mark.asyncio
async def test_concurrency_limit(app):
    transport = httpx.ASGITransport(app=app)
    
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        tasks = [client.get("/ping") for _ in range(100)]
        responses = await asyncio.gather(*tasks)

        status_codes = [r.status_code for r in responses]
        counts = Counter(status_codes)
        
        print("\n--- STATUS CODE COUNTS ---")
        print(counts)
        print("--------------------------\n")
        
        success_count = counts.get(200, 0)
        limited_count = counts.get(429, 0)

        assert success_count == 10, f"Expected 10 successes, got {success_count}"
        assert limited_count == 90, f"Expected 90 rate limits, got {limited_count}"