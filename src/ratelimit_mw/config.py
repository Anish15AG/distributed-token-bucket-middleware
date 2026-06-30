from dataclasses import dataclass

@dataclass
class RateLimitConfig:

    # Maximum tokens a bucket can hold
    capacity: int = 10

    # Refill rate of tokens
    refill_rate: float = 1.0

    # Redis connection string
    redis_url: str = "redis://localhost:6379/0"