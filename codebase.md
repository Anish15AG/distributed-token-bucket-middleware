# .gitignore

```
__pycache__/
*.py[cod]
*$py.class

# Virtual environments
venv/
env/
.venv/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Testing
.pytest_cache/
.coverage
htmlcov/

# OS
.DS_Store

# Local config
.env
EOF

git add .gitignore
git commit -m "Initial commit: Add .gitignore"
codebase.md

```

# .pytest_cache/.gitignore

```
# Created by pytest automatically.
*

```

# .pytest_cache/CACHEDIR.TAG

```TAG
Signature: 8a477f597d28d172789f06886806bc55
# This file is a cache directory tag created by pytest.
# For information about cache directory tags, see:
#	https://bford.info/cachedir/spec.html

```

# .pytest_cache/README.md

```md
# pytest cache directory #

This directory contains data from the pytest's cache plugin,
which provides the `--lf` and `--ff` options, as well as the `cache` fixture.

**Do not** commit this to version control.

See [the docs](https://docs.pytest.org/en/stable/how-to/cache.html) for more information.

```

# .pytest_cache/v/cache/lastfailed

```
{}
```

# .pytest_cache/v/cache/nodeids

```
[
  "tests/test_concurrency.py::test_concurrency_limit"
]
```

# demo_app_2/main.py

```py
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
```

# demo_app/main.py

```py
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
    import asyncio
    await asyncio.sleep(3)
    # time.sleep(random.uniform(0.1, 0.3))
    return {"data": [1, 2, 3, 4, 5], "timestamp": time.time()}
```

# pyproject.toml

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "ratelimit-mw"
version = "0.1.0"
description = "A cost-aware, adaptive rate limiter ASGI middleware for FastAPI"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
keywords = ["fastapi", "rate-limiting", "asgi", "middleware", "redis"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Framework :: FastAPI",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

dependencies = [
    "fastapi>=0.100.0",
    "redis>=5.0.0",
    "starlette>=0.27.0",
    "uvicorn>=0.23.0",
    "httpx>=0.24.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "httpx>=0.24.0",
    "black>=23.0.0",
    "ruff>=0.0.290",
]

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]

[tool.black]
line-length = 88
target-version = ["py38"]

[tool.ruff]
line-length = 88
select = ["E", "F", "I"]
```

# README.md

```md

```

# src/ratelimit_mw.egg-info/dependency_links.txt

```txt


```

# src/ratelimit_mw.egg-info/PKG-INFO

```
Metadata-Version: 2.4
Name: ratelimit-mw
Version: 0.1.0
Summary: A cost-aware, adaptive rate limiter ASGI middleware for FastAPI
Author-email: Your Name <your.email@example.com>
License: MIT
Keywords: fastapi,rate-limiting,asgi,middleware,redis
Classifier: Development Status :: 3 - Alpha
Classifier: Framework :: FastAPI
Classifier: Intended Audience :: Developers
Classifier: License :: OSI Approved :: MIT License
Classifier: Programming Language :: Python :: 3
Classifier: Programming Language :: Python :: 3.8
Classifier: Programming Language :: Python :: 3.9
Classifier: Programming Language :: Python :: 3.10
Classifier: Programming Language :: Python :: 3.11
Classifier: Programming Language :: Python :: 3.12
Requires-Python: >=3.8
Description-Content-Type: text/markdown
Requires-Dist: fastapi>=0.100.0
Requires-Dist: redis>=5.0.0
Requires-Dist: starlette>=0.27.0
Requires-Dist: uvicorn>=0.23.0
Requires-Dist: httpx>=0.24.0
Provides-Extra: dev
Requires-Dist: pytest>=7.4.0; extra == "dev"
Requires-Dist: pytest-asyncio>=0.21.0; extra == "dev"
Requires-Dist: httpx>=0.24.0; extra == "dev"
Requires-Dist: black>=23.0.0; extra == "dev"
Requires-Dist: ruff>=0.0.290; extra == "dev"

```

# src/ratelimit_mw.egg-info/requires.txt

```txt
fastapi>=0.100.0
redis>=5.0.0
starlette>=0.27.0
uvicorn>=0.23.0
httpx>=0.24.0

[dev]
pytest>=7.4.0
pytest-asyncio>=0.21.0
httpx>=0.24.0
black>=23.0.0
ruff>=0.0.290

```

# src/ratelimit_mw.egg-info/SOURCES.txt

```txt
README.md
pyproject.toml
src/ratelimit_mw/__init__.py
src/ratelimit_mw/config.py
src/ratelimit_mw/middleware.py
src/ratelimit_mw.egg-info/PKG-INFO
src/ratelimit_mw.egg-info/SOURCES.txt
src/ratelimit_mw.egg-info/dependency_links.txt
src/ratelimit_mw.egg-info/requires.txt
src/ratelimit_mw.egg-info/top_level.txt
tests/test_concurrency.py
tests/test_middleware.py
```

# src/ratelimit_mw.egg-info/top_level.txt

```txt
ratelimit_mw

```

# src/ratelimit_mw/__init__.py

```py
from .middleware import RateLimitMiddleware

__all__ = ["RateLimitMiddleware"]
```

# src/ratelimit_mw/config.py

```py
from dataclasses import dataclass
from typing import Callable
from starlette.requests import Request

def default_key_resolver(request: Request) -> str:
    # Identifying users by their IP
    return request.client.host if request.client else "unknown"

def default_org_resolver(request: Request) -> str:
    return "default_org"

def default_cost_resolver(requst: Request) -> int:
    # Cost of each requst is 1 Token
    return 1


@dataclass
class RateLimitConfig:

    # Maximum tokens a bucket can hold
    capacity: int = 10

    # Refill rate of tokens
    refill_rate: float = 1.0

    # Redis connection string
    redis_url: str = "redis://localhost:6379/0"

    # Pluggable Resolver
    key_resolver : Callable[[Request], str] = default_key_resolver
    cost_resolver : Callable[[Request], int] = default_cost_resolver
    org_resolver : Callable[[Request], str] = default_org_resolver

    # Load Sheding config
    health_check_url: str | None = None
    health_check_interval: float = 5.0
    max_load_factor: float = 3.0
```

# src/ratelimit_mw/middleware.py

```py
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
```

# tests/__init__.py

```py

```

# tests/test_concurrency.py

```py
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
```

# tests/test_middleware.py

```py

```

