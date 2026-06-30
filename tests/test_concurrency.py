import asyncio
import pytest
import httpx
from fastapi import FastAPI
from ratelimit_mw import RateLimitMiddleware
from ratelimit_mw.config import RateLimitConfig

@pytest.fixture
def app():
    application = FastAPI()

    @application.get("/ping")
    async def ping():
        return {"msg" : "pong"}
    
    config = RateLimitConfig(capacity=10, refill_rate=0.1)
    application.add_middleware(RateLimitMiddleware, config=config)
    return application

@pytest.mark.asyncio
async def test_concurrency_limit(app):
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        tasks = [client.get("/ping") for _ in range(100)]

        responses = await asyncio.gather(*tasks)

        status_codes = [r.status_code for r in responses]
        success_count = status_codes.count(200)
        limited_count = status_codes.count(429)


        assert success_count == 10, f"Expected 10 successes, got {success_count}"
        assert limited_count == 90, f"Expected 90 rate limits, got {limited_count}"