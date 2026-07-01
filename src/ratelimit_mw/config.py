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