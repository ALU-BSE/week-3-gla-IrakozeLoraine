from flask import Flask, render_template, jsonify
import time
from utils.calculator import benchmark_fibonacci
from models.database import init_db
from models.products import get_products
from datetime import datetime, timedelta
from flask import make_response, request
from redis import Redis
from flask_caching import Cache

# Initialize database on startup
init_db()

app = Flask(__name__)
# Add to your Flask app configuration
app.config['REDIS_URL'] = 'redis://localhost:6379/0'
redis_client = Redis.from_url(app.config['REDIS_URL'])

# Configure caching
cache_config = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_REDIS_URL": "redis://localhost:6379/0",
    "CACHE_DEFAULT_TIMEOUT": 300
}
cache = Cache(app, config=cache_config)

# Make redis_client available to other modules
app.extensions['redis'] = redis_client

@app.route('/')
def index():
    # Simulate a slow operation
    time.sleep(2)
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    # Simulate expensive data retrieval
    time.sleep(1)
    data = {
        'items': [
            {'id': 1, 'name': 'Item 1'},
            {'id': 2, 'name': 'Item 2'},
            {'id': 3, 'name': 'Item 3'}
        ],
        'timestamp': time.time()
    }
    return jsonify(data)

@app.route('/benchmark')
def benchmark():
    results = benchmark_fibonacci()
    return render_template('benchmark.html', results=results)

@app.route('/products')
def product_list():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    use_cache = request.args.get('cache', 'true').lower() != 'false'
    
    result = get_products(page, per_page, use_cache)
    
    return render_template('products.html', 
            products=result['products'], 
            pagination=result['pagination'],
            query_time=result['query_time'],
            use_cache=use_cache)

@app.route('/products/<int:product_id>')
def product_detail(product_id):
    use_cache = request.args.get('cache', 'true').lower() != 'false'
    result = get_product_by_id(product_id, use_cache)
    
    if not result:
        return "Product not found", 404
    
    return render_template('product_detail.html', 
            product=result['product'],
            query_time=result['query_time'],
            use_cache=use_cache)

@app.route('/static-content')
def static_content():
    """Example of content that rarely changes"""
    content = "<h1>Static Content</h1><p>This content rarely changes and can be cached for a long time.</p>"
    
    # Create response
    response = make_response(render_template('static_content.html', content=content))
    
    # Set Cache-Control header
    # max-age=3600: Cache for 1 hour (3600 seconds)
    # public: Can be cached by browsers and intermediate caches
    response.headers['Cache-Control'] = 'public, max-age=3600'
    
    # Set Expires header
    response.headers['Expires'] = (datetime.utcnow() + timedelta(hours=1)).strftime('%a, %d %b %Y %H:%M:%S GMT')
    
    return response

@app.route('/dynamic-content')
def dynamic_content():
    """Example of content that changes frequently"""
    # Generate dynamic content with current timestamp
    now = datetime.utcnow()
    content = f"<h1>Dynamic Content</h1><p>Generated at: {now.strftime('%H:%M:%S')}</p>"
    
    # Create response
    response = make_response(render_template('dynamic_content.html', content=content))
    
    # Set Cache-Control header
    # no-cache: Must revalidate with server before using cached version
    # must-revalidate: Don't use stale cached version without checking with server first
    response.headers['Cache-Control'] = 'no-cache, must-revalidate'
    
    # Set Last-Modified header
    response.headers['Last-Modified'] = now.strftime('%a, %d %b %Y %H:%M:%S GMT')
    
    return response

@app.route('/conditional-content')
def conditional_content():
    """Example of conditional caching with ETag"""
    # Generate content
    content = "<h1>Conditional Content</h1><p>This content uses ETags for efficient caching.</p>"
    
    # Generate an ETag (in a real app, this would be based on the content)
    etag = f"v1-{hash(content)}"
    
    # Check if the client sent an If-None-Match header matching our ETag
    if request.headers.get('If-None-Match') == etag:
        # The client already has the current version
        return '', 304  # 304 Not Modified
    
    # Create response
    response = make_response(render_template('conditional_content.html', content=content))
    
    # Set ETag and Cache-Control headers
    response.headers['ETag'] = etag
    response.headers['Cache-Control'] = 'public, max-age=300'  # Cache for 5 minutes
    
    return response

@app.route('/products/compare')
def compare_caching():
    page = int(request.args.get('page', 1))
    
    # Time Redis caching
    start = time.time()
    redis_result = get_products_redis(page)
    redis_time = time.time() - start
    
    # Time simple in-memory caching
    start = time.time()
    memory_result = get_products(page, per_page=10, use_cache=True)
    memory_time = time.time() - start
    
    # Time uncached
    start = time.time()
    uncached_result = get_products(page, per_page=10, use_cache=False)
    uncached_time = time.time() - start
    
    return render_template('compare_caching.html',
        redis_time=redis_time,
        memory_time=memory_time,
        uncached_time=uncached_time,
        page=page)

@app.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
def edit_product(product_id):
    if request.method == 'POST':
        name = request.form.get('name')
        price = float(request.form.get('price'))
        description = request.form.get('description')
        
        if update_product(product_id, name=name, price=price, description=description):
            flash('Product updated successfully!', 'success')
            return redirect(url_for('product_detail', product_id=product_id))
        else:
            flash('Failed to update product', 'error')
    
    product = get_product_by_id(product_id, use_cache=False)['product']
    return render_template('edit_product.html', product=product)

@app.route('/expensive-view')
@cache.cached(timeout=60)
def expensive_view():
    time.sleep(3)  # Simulate expensive operation
    return "This view took a long time to generate at: " + str(time.time())

@cache.memoize(timeout=60)
def expensive_function(param1, param2):
    time.sleep(2)
    return f"Result for {param1} and {param2} at {time.time()}"

@app.route('/api/weather')
@cache.cached(timeout=60, query_string=True)
def weather_api():
    # Simulate API call to external weather service
    time.sleep(1)
    
    # In a real app, this would call an actual weather API
    return jsonify({
        "temperature": 72 + (time.time() % 10) - 5,  # Random-ish value
        "conditions": ["sunny", "cloudy", "rainy"][int(time.time() % 3)],
        "timestamp": time.time(),
        "source": "cache" if request.args.get('cached') else "live"
    })

@app.route('/weather')
def weather_demo():
    return render_template('weather.html')

if __name__ == '__main__':
    app.run(debug=True)