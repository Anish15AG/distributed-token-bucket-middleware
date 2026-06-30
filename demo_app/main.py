from fastapi import FastAPI
import time
import random

from ratelimit_mw import RateLimitMiddleware
from ratelimit_mw.config import RateLimitConfig

app = FastAPI(title="Rate Limiter Middleware Demo", version="1.0.0")

rate_limit_config = RateLimitConfig(capacity=5, refill_rate=1.0)
app.add_middleware(RateLimitMiddleware, config=rate_limit_config)

@app.get("/ping")
async def ping():
    return {"message": "pong", "timestamp": time.time()}

@app.get("/data")
async def get_data():
    time.sleep(random.uniform(0.1, 0.3))
    return {"data": [1, 2, 3, 4, 5], "timestamp": time.time()}