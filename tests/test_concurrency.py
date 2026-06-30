import asyncio
import pytest
import httpx
from redis.asyncio import aioredis
from collections import Counter
from fastapi import FastAPI
from ratelimit_mw import RateLimitMiddleware
from ratelimit_mw.config import RateLimitConfig

@pytest.fixture(autouse=True)
async def clean_redis():
    client = aioredis.from_url("redis://localhost:6379/1", decode_responses = True)
    await client.flushdb()
    yield
    await client.flushdb()
    await client.aclose()


def app():
    application = FastAPI()

    @application.get("/ping")
    async def ping():
        return {"msg" : "pong"}
    
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

        print("--Status Code Counts--")
        print(counts)
        print("-----\n")

        for r in responses:
            if r.status_code not in (200,429):
                print("Unexpected Error {r.status_code}: {r.text}")

        success_count = counts.count(200)
        limited_count = counts.count(429)


        assert success_count == 10, f"Expected 10 successes, got {success_count}"
        assert limited_count == 90, f"Expected 90 rate limits, got {limited_count}"