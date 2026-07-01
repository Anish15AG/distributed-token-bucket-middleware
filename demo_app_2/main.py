from fastapi import FastAPI, Request
import time
from ratelimit_mw import RateLimitMiddleware
from ratelimit_mw.config import RateLimitConfig

def custom_org_resolver(request: Request) -> str:
    api_key = request.headers.get("X-API-Key", "anonymous")
    
    if api_key == "client_A":
        return "org_premium"
    elif api_key == "client_B":
        return "org_premium"
    return "org_free"

def api_key_resolver(request: Request) -> str:
    return request.headers.get("X-API-Key", "anonymous")

def route_cost_resolver(request: Request) -> int:
    if request.url.path == "/heavy":
        return 5
    return 1

app = FastAPI(title="API Key & Cost-Aware Demo App")

config = RateLimitConfig(
    capacity=5,
    refill_rate=1.0,
    key_resolver=api_key_resolver,
    cost_resolver=route_cost_resolver,
    org_resolver=custom_org_resolver,
)

app.add_middleware(RateLimitMiddleware, config=config)

@app.get("/ping")
async def ping():
    return {"message": "pong - Cost: 1 token"}

@app.get("/heavy")
async def heavy():
    time.sleep(0.5)
    return {"message": "Heavy computation task - Cost: 5 tokens"}