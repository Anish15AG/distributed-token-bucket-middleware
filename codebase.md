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
{
  "tests/test_concurrency.py::test_concurrency_limit": true
}
```

# .pytest_cache/v/cache/nodeids

```
[
  "tests/test_concurrency.py::test_concurrency_limit"
]
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
    time.sleep(random.uniform(0.1, 0.3))
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
src/ratelimit_mw/middleware.py
src/ratelimit_mw.egg-info/PKG-INFO
src/ratelimit_mw.egg-info/SOURCES.txt
src/ratelimit_mw.egg-info/dependency_links.txt
src/ratelimit_mw.egg-info/requires.txt
src/ratelimit_mw.egg-info/top_level.txt
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

@dataclass
class RateLimitConfig:

    # Maximum tokens a bucket can hold
    capacity: int = 10

    # Refill rate of tokens
    refill_rate: float = 1.0

    # Redis connection string
    redis_url: str = "redis://localhost:6379/0"
```

# src/ratelimit_mw/middleware.py

```py
import time
import redis.asyncio as aioredis
from redis.exceptions import WatchError
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

    async def dispatch(self, request: Request, call_next) -> Response:
        identity = request.client.host if request.client else "unknown"
        bucket_key = f"ratelimit:{identity}"
        cost = 1

        # Check and consume tokens
        allowed, remaining, retry_after = await self._process_bucket(bucket_key, cost)

        if not allowed:
            return JSONResponse(
                status_code=429,
                content={"error": "Rate Limit exceeded. Please try again later"},
                headers={"Retry-After": str(int(retry_after) + 1)},
            )

        # Pass request to the app
        response = await call_next(request)

        response.headers["X-RateLimit-Limit"] = str(self.config.capacity)
        response.headers["X-RateLimit-Remaining"] = str(int(remaining))
        
        return response

    async def _process_bucket(self, bucket_key: str, cost: int):
        capacity = self.config.capacity
        refill_rate = self.config.refill_rate

        while True:
            try:
                # Create a pipeline and WATCH the key for changes
                pipe = self.redis.pipeline(transaction=True)
                await pipe.watch(bucket_key)

                # Read current state
                bucket_state = await pipe.hgetall(bucket_key)
                now = time.time()

                if not bucket_state:
                    current_tokens = float(capacity - cost)
                    last_refill = now
                else:
                    stored_tokens = float(bucket_state.get("tokens", 0))
                    last_refill = float(bucket_state.get("last_refill", now))
                    time_passed = now - last_refill
                    tokens_to_add = time_passed * refill_rate
                    current_tokens = min(capacity, stored_tokens + tokens_to_add)

                # Check if user has enough tokens
                if current_tokens < cost:
                    await pipe.unwatch()
                    tokens_needed = cost - current_tokens
                    retry_after = tokens_needed / refill_rate
                    return False, current_tokens, retry_after

                # Consume token
                current_tokens -= cost

                # Execute the transaction atomically
                pipe.multi()
                pipe.hset(bucket_key, mapping={
                    "tokens": str(current_tokens),
                    "last_refill": str(now)
                })
                pipe.expire(bucket_key, 60)
                
                await pipe.execute()

                return True, current_tokens, 0

            except WatchError:
                # Another request modified the key concurrently. 
                # The loop will automatically retry from the beginning.
                continue
            finally:
                # Reset the pipeline to return the connection to the pool
                await pipe.reset()
```

# tests/__init__.py

```py

```

# tests/test_concurrency.py

```py
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
        assert limited_count == 90, f"Expected 90 rate limits, got {success_count}"
```

# tests/test_middleware.py

```py

```

