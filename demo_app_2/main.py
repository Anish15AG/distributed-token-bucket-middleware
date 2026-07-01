from fastapi import FastAPI, Request
import time
from ratelimit_mw import RateLimitMiddleware
from ratelimit_mw.config import RateLimitConfig

def api_key_resolver(request: Request) -> int:
    return request.headers.get("X-API-Key", "anonymous")

def route_cost_resolver(request: Request) -> int:
    if request.url.path == "/heavy":
        return 5
    return 1

app = FastAPI(title="API Key & Cost-Aware Demo App")

config = RateLimitConfig(
    capacity=10,
    refill_rate=1.0,
    key_resolver=api_key_resolver,
    cost_resolver=route_cost_resolver,
)

app.add_middleware(RateLimitMiddleware, config=config)

@app.get("/ping")
async def ping():
    return {"message":"pong - Cost: 1 token for this transaction"}

@app.get("/heavy")
async def heavy():
    time.sleep(0.5)
    return {"message":"Heavy computation task - Cost: 5 tokens for this transaction"}