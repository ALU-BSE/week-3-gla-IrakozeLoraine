import time
from models.database import get_db_connection
from utils.redis_cache import redis_cache

# Simple in-memory cache
_cache = {}

def get_products(page=1, per_page=10, use_cache=True):
    """Get a paginated list of products, with optional caching"""
    cache_key = f'products_page_{page}_per_page_{per_page}'
    
    # Check cache first if caching is enabled
    if use_cache and cache_key in _cache:
        cache_entry = _cache[cache_key]
        # Check if cache is still valid (30 seconds TTL)
        if time.time() - cache_entry['timestamp'] < 30:
            print("Cache hit!")
            return cache_entry['data']
        else:
            print("Cache expired!")
    else:
        print("Cache miss!")
    
    # Cache miss or expired, query the database
    start_time = time.time()
    
    with get_db_connection() as conn:
        offset = (page - 1) * per_page
        query = '''
            SELECT id, name, price 
            FROM products 
            ORDER BY id 
            LIMIT ? OFFSET ?
        '''
        rows = conn.execute(query, (per_page, offset)).fetchall()
        
        # Convert to list of dictionaries
        products = [dict(row) for row in rows]
        
        # Get total count for pagination
        total = conn.execute('SELECT COUNT(*) FROM products').fetchone()[0]
    
    query_time = time.time() - start_time
    
    result = {
        'products': products,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page
        },
        'query_time': query_time
    }
    
    # Update cache
    if use_cache:
        _cache[cache_key] = {
            'data': result,
            'timestamp': time.time()
        }
    
    return result

def get_product_by_id(product_id, use_cache=True):
    """Get a product by ID with caching"""
    cache_key = f'product_{product_id}'
    
    # Check cache first if caching is enabled
    if use_cache and cache_key in _cache:
        cache_entry = _cache[cache_key]
        # Check if cache is still valid (1 minute TTL)
        if time.time() - cache_entry['timestamp'] < 60:
            print(f"Cache hit for product {product_id}!")
            return cache_entry['data']
        else:
            print(f"Cache expired for product {product_id}!")
    else:
        print(f"Cache miss for product {product_id}!")
    
    # Cache miss or expired, query the database
    start_time = time.time()
    
    with get_db_connection() as conn:
        # Simulate a complex query with SLEEP
        query = '''
            SELECT * FROM products WHERE id = ?
        '''
        # Simulate a complex join or slow query
        time.sleep(0.5)  
        product = conn.execute(query, (product_id,)).fetchone()
        
        if product is None:
            return None
        
        product = dict(product)
    
    query_time = time.time() - start_time
    
    result = {
        'product': product,
        'query_time': query_time
    }
    
    # Update cache
    if use_cache:
        _cache[cache_key] = {
            'data': result,
            'timestamp': time.time()
        }
    
    return result

@redis_cache('products_list', ttl=30)
def get_products_redis(page=1, per_page=10):
    """Get paginated products with Redis caching"""
    with get_db_connection() as conn:
        offset = (page - 1) * per_page
        query = '''
            SELECT id, name, price 
            FROM products 
            ORDER BY id 
            LIMIT ? OFFSET ?
        '''
        rows = conn.execute(query, (per_page, offset)).fetchall()
        products = [dict(row) for row in rows]
        total = conn.execute('SELECT COUNT(*) FROM products').fetchone()[0]
    
    return {
        'products': products,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page
        }
    }

def get_with_stampede_protection(key, ttl, fallback_function, lock_timeout=5):
    """
    Get data with protection against cache stampede (dog-piling effect)
    """
    # Try to get cached data
    cached_data = cache.get(key)
    if cached_data is not None:
        return json.loads(cached_data)
    
    # Try to acquire lock
    lock_key = f"{key}:lock"
    if cache.setnx(lock_key, "locked"):
        # Set lock expiration
        cache.expire(lock_key, lock_timeout)
        
        try:
            # Generate fresh data
            fresh_data = fallback_function()
            cache.setex(key, ttl, json.dumps(fresh_data))
            return fresh_data
        finally:
            # Release lock
            cache.delete(lock_key)
    else:
        # Wait for lock to release
        time.sleep(0.1)
        return get_with_stampede_protection(key, ttl, fallback_function, lock_timeout)

def get_multiple_products(product_ids):
    """Get multiple products efficiently using Redis pipeline"""
    pipeline = cache.pipeline()
    
    # Queue up all the GET commands
    for product_id in product_ids:
        pipeline.get(f"product_{product_id}")
    
    # Execute all commands in one network roundtrip
    cached_results = pipeline.execute()
    
    results = []
    for product_id, cached_data in zip(product_ids, cached_results):
        if cached_data is not None:
            results.append(json.loads(cached_data))
        else:
            # Fallback to database for cache misses
            product = get_product_from_db(product_id)
            if product:
                # Cache for future requests
                cache.setex(f"product_{product_id}", 60, json.dumps(product)))
                results.append(product)
    
    return results

def update_product(product_id, name=None, price=None, description=None):
    """Update product and invalidate cache"""
    with get_db_connection() as conn:
        # Update database
        updates = []
        params = []
        
        if name is not None:
            updates.append("name = ?")
            params.append(name)
        if price is not None:
            updates.append("price = ?")
            params.append(price)
        if description is not None:
            updates.append("description = ?")
            params.append(description)
        
        if not updates:
            return False
        
        query = f"UPDATE products SET {', '.join(updates)} WHERE id = ?"
        params.append(product_id)
        conn.execute(query, params)
        conn.commit()
    
    # Invalidate cache
    redis_client = current_app.extensions['redis']
    
    # Delete specific product cache
    redis_client.delete(f"product_{product_id}")
    
    # Delete all product list caches (using a pattern)
    keys = redis_client.keys("products_list:*")
    if keys:
        redis_client.delete(*keys)
    
    return True


