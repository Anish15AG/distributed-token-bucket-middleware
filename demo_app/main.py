from fastapi import FastAPI
import time
import random
from ratelimit_mw import RateLimitMiddleware

app = FastAPI(title="Rate Limiter Middleware Demo", version="1.0.0")

@app.get("/ping")
async def ping():
    "A cheap, lightweight endpoint to test rate limiting middleware"
    return {"message": "pong", "timestamp": time.time()}

@app.get("/data")
async def get_data():
    """A slightly more expensive endpoint (simulated)"""
    time.sleep(random.uniform(0.1, 0.3))
    return {"data": [1, 2, 3, 4, 5], "timestamp": time.time()}

@app.get("/heavy")
async def heavy_computation():
    """A very expensive endpoint."""
    time.sleep(random.uniform(0.5, 1.0))
    return {"result": "heavy computation done", "timestamp": time.time()}

app.add_middleware(RateLimitMiddleware)