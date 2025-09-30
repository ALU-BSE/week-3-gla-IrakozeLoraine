import json
import time
from functools import wraps
from flask import current_app

def redis_cache(key_prefix, ttl=60):
    """
    Decorator to cache function results in Redis
    
    Args:
        key_prefix: Prefix for cache keys
        ttl: Time-to-live in seconds
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"{key_prefix}:{str(args)}:{str(kwargs)}"
            
            # Try to get cached data
            redis_client = current_app.extensions['redis']
            cached_data = redis_client.get(cache_key)
            
            if cached_data is not None:
                return json.loads(cached_data)
            
            # Cache miss - call original function
            result = f(*args, **kwargs)
            
            # Store in Redis
            redis_client.setex(cache_key, ttl, json.dumps(result))
            
            return result
        return wrapper
    return decorator
