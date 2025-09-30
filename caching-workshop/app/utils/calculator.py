import time
from functools import lru_cache

def fibonacci_uncached(n):
    """Calculate the nth Fibonacci number (inefficient recursive implementation)"""
    if n <= 1:
        return n
    return fibonacci_uncached(n-1) + fibonacci_uncached(n-2)

@lru_cache(maxsize=128)
def fibonacci_cached(n):
    """Calculate the nth Fibonacci number with caching"""
    if n <= 1:
        return n
    return fibonacci_cached(n-1) + fibonacci_cached(n-2)

def benchmark_fibonacci():
    """Compare the performance of cached vs uncached implementations"""
    n = 30
    
    # Benchmark uncached version
    start = time.time()
    result_uncached = fibonacci_uncached(n)
    uncached_time = time.time() - start
    
    # Benchmark cached version
    start = time.time()
    result_cached = fibonacci_cached(n)
    cached_time = time.time() - start
    
    return {
        'n': n,
        'result': result_cached,
        'uncached_time': uncached_time,
        'cached_time': cached_time,
        'speedup_factor': uncached_time / cached_time if cached_time > 0 else 'infinite'
    }