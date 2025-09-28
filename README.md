[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=20758009)
# Guided Learning Activity - Caching in Web Applications with Python

## Introduction

Welcome to this comprehensive guide on implementing caching in web applications using Python! Whether you're building a personal blog, an e-commerce platform, or a content management system, understanding and implementing caching is essential for creating performant web applications that can scale.

In this guide, you'll learn:
- What caching is and why it's important
- Different types of caching strategies
- How to implement various caching mechanisms in Python web applications
- Best practices for cache management
- How to measure the impact of your caching implementations
- Common pitfalls and how to avoid them

By the end of this guide, you'll have hands-on experience implementing different caching strategies and will be able to apply these concepts to your own projects.

## Table of Contents

1. [Understanding Caching Fundamentals](#understanding-caching-fundamentals)
2. [Types of Caching](#types-of-caching)
3. [Setting Up Your Development Environment](#setting-up-your-development-environment)
4. [In-Memory Caching with Python](#in-memory-caching-with-python)
5. [Database Query Caching](#database-query-caching)
6. [HTTP Caching](#http-caching)
7. [Implementing Redis for Distributed Caching](#implementing-redis-for-distributed-caching)
8. [Cache Invalidation Strategies](#cache-invalidation-strategies)
9. [Caching in Flask Applications](#caching-in-flask-applications)
10. [Caching in Django Applications](#caching-in-django-applications)
11. [Monitoring and Optimizing Your Cache](#monitoring-and-optimizing-your-cache)
12. [Additional Resources](#additional-resources)

## Understanding Caching Fundamentals

### What is Caching?

Caching is the process of storing copies of data in a temporary storage location (a cache) so future requests for that data can be served faster. The primary purpose of caching is to increase data retrieval performance by reducing the need to access the underlying slower storage layer.

### Why is Caching Important?

1. **Performance Improvement**: Caching reduces latency and improves application response time.
2. **Reduced Server Load**: By serving cached data, you reduce the load on your database and application servers.
3. **Bandwidth Savings**: Less data needs to be transferred between servers and clients.
4. **Improved User Experience**: Faster load times lead to better user satisfaction.
5. **Cost Efficiency**: Reduced computational needs can lower infrastructure costs.

### Key Caching Concepts

- **Cache Hit**: When requested data is found in the cache.
- **Cache Miss**: When requested data is not found in the cache and must be fetched from the original source.
- **Cache Expiration**: When cached data is considered stale and needs to be refreshed.
- **Cache Invalidation**: The process of removing or updating cached data when the original data changes.
- **Cache Eviction**: When items are removed from the cache due to space constraints.
- **Cache Hit Ratio**: The percentage of requests that are served from the cache versus those that require fetching from the original source.

### Exercise 1: Analyzing Caching Potential

**Objective**: Identify opportunities for caching in a sample application.

1. Clone this sample Flask blog application:
```bash
git clone https://github.com/iPelino/afretec_event_locator_api
cd afretec_event_locator_api
pip install -r requirements.txt
```

2. Run the application and use a tool like Chrome DevTools or Firefox Developer Tools to analyze the network performance.

3. Create a document identifying:
   - Which resources could benefit from caching
   - What type of caching would be appropriate for each resource
   - Expected performance improvements if caching was implemented

## Types of Caching

### Browser Caching

Browser caching stores static assets (CSS, JavaScript, images) locally in the user's browser, reducing the need to download them on subsequent visits.

### Application Caching

Application caching occurs within your web application and includes:

- **Memory Caching**: Storing data in the application's memory for quick access
- **Database Query Caching**: Storing the results of expensive database queries
- **Computed Results Caching**: Storing the results of complex calculations

### Distributed Caching

Distributed caching uses external systems like Redis or Memcached to store cached data, allowing multiple application instances to share the same cache.

### Content Delivery Networks (CDNs)

CDNs cache content at strategically placed physical nodes across different geographical locations to deliver content to users more quickly and reliably.

### Exercise 2: Comparing Caching Strategies

**Objective**: Understand the trade-offs between different caching strategies.

Create a comparison table of different caching strategies with the following criteria:
- Implementation complexity
- Performance impact
- Scalability
- Data consistency challenges
- Appropriate use cases

## Setting Up Your Development Environment

To follow along with the hands-on exercises in this guide, you'll need to set up a Python development environment with the necessary tools.

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment tool (venv or conda)
- Git
- A code editor (VS Code, PyCharm, etc.)

### Setup Steps

1. Create a new project directory:
```bash
mkdir caching-workshop
cd caching-workshop
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install Flask Flask-Caching redis SQLAlchemy requests pytest
```

4. Create a basic project structure:
```bash
mkdir -p app/templates app/static app/models app/utils tests
touch app/__init__.py app/models/__init__.py app/utils/__init__.py
touch app/app.py
```

### Exercise 3: Setting Up a Basic Flask Application

**Objective**: Create a simple Flask application that we'll use to implement various caching strategies.

1. Create a basic Flask app in `app/app.py`:

```python
from flask import Flask, render_template, jsonify
import time

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
```

2. Create a simple template in `app/templates/index.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Caching Demo</title>
</head>
<body>
    <h1>Caching Workshop</h1>
    <div id="data-container">Loading...</div>
    
    <script>
        // Simple script to fetch data from our API
        fetch('/api/data')
            .then(response => response.json())
            .then(data => {
                document.getElementById('data-container').innerHTML = 
                    `<pre>${JSON.stringify(data, null, 2)}</pre>`;
            });
    </script>
</body>
</html>
```

3. Run the application:
```bash
python app/app.py
```

4. Visit http://localhost:5000 in your browser and note the loading time.

## In-Memory Caching with Python

The simplest form of caching is to store data in memory. Python provides several ways to implement in-memory caching.

### Using Python's `functools.lru_cache`

The `lru_cache` decorator from the `functools` module provides a simple way to cache function results in memory using a Least Recently Used (LRU) cache strategy.

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_expensive_data(param):
    # Expensive operation here
    import time
    time.sleep(2)  # Simulate long processing
    return f"Result for {param}"

# First call - will be slow
result1 = get_expensive_data("test")
print(result1)

# Second call with same parameter - will be fast (cached)
result2 = get_expensive_data("test")
print(result2)

# Different parameter - will be slow again
result3 = get_expensive_data("another_test")
print(result3)
```

### Creating a Simple Cache Class

For more control, you can implement your own caching mechanism:

```python
class SimpleCache:
    def __init__(self, max_size=100):
        self.cache = {}
        self.max_size = max_size
    
    def get(self, key, default=None):
        return self.cache.get(key, default)
    
    def set(self, key, value, ttl=None):
        # Basic eviction strategy - if cache is full, remove oldest item
        if len(self.cache) >= self.max_size:
            # In a real implementation, you'd want a more sophisticated strategy
            self.cache.pop(next(iter(self.cache)))
        
        self.cache[key] = {
            'value': value,
            'expires_at': time.time() + ttl if ttl else None
        }
    
    def delete(self, key):
        if key in self.cache:
            del self.cache[key]
    
    def is_valid(self, key):
        if key not in self.cache:
            return False
        
        item = self.cache[key]
        if item['expires_at'] and time.time() > item['expires_at']:
            self.delete(key)
            return False
        
        return True

# Usage
cache = SimpleCache()
cache.set('user:1', {"name": "John", "email": "john@example.com"}, ttl=60)  # Cache for 60 seconds

if cache.is_valid('user:1'):
    user = cache.get('user:1')
    print(user)
```

### Exercise 4: Implementing Function-Level Caching

**Objective**: Improve the performance of a function that performs expensive calculations.

1. Create a new file `app/utils/calculator.py` with a function that performs a "costly" operation:

```python
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
```

2. Create a route in `app/app.py` to display the benchmark results:

```python
from app.utils.calculator import benchmark_fibonacci

@app.route('/benchmark')
def benchmark():
    results = benchmark_fibonacci()
    return render_template('benchmark.html', results=results)
```

3. Create a template in `app/templates/benchmark.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Fibonacci Caching Benchmark</title>
    <style>
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .highlight { background-color: #e6ffe6; }
    </style>
</head>
<body>
    <h1>Fibonacci Caching Benchmark</h1>
    <table>
        <tr>
            <th>Parameter (n)</th>
            <td>{{ results.n }}</td>
        </tr>
        <tr>
            <th>Result (Fibonacci number)</th>
            <td>{{ results.result }}</td>
        </tr>
        <tr>
            <th>Uncached Time (seconds)</th>
            <td>{{ "%.4f"|format(results.uncached_time) }}</td>
        </tr>
        <tr class="highlight">
            <th>Cached Time (seconds)</th>
            <td>{{ "%.4f"|format(results.cached_time) }}</td>
        </tr>
        <tr class="highlight">
            <th>Speedup Factor</th>
            <td>{% if results.speedup_factor == 'infinite' %}∞{% else %}{{ "%.2f"|format(results.speedup_factor) }}x{% endif %}</td>
        </tr>
    </table>
    
    <h2>Explanation</h2>
    <p>
        The uncached Fibonacci implementation recalculates each value multiple times, leading to exponential time complexity.
        The cached version using <code>@lru_cache</code> stores results of previous calculations, dramatically improving performance.
    </p>
</body>
</html>
```

4. Run the application and visit http://localhost:5000/benchmark to see the dramatic difference caching makes.

## Database Query Caching

Database queries are often expensive operations that benefit greatly from caching. Let's explore how to implement database query caching in Python.

### Setting Up a Database

First, let's set up a simple SQLite database for our exercises:

```python
# app/models/database.py
import sqlite3
import time
from contextlib import contextmanager

DATABASE_PATH = 'app.db'

def init_db():
    """Initialize the database with sample data"""
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Check if we need to insert sample data
        if conn.execute('SELECT COUNT(*) FROM products').fetchone()[0] == 0:
            # Insert 1000 sample products
            for i in range(1, 1001):
                conn.execute(
                    'INSERT INTO products (name, description, price) VALUES (?, ?, ?)',
                    (f'Product {i}', f'Description for product {i}', i * 10.99)
                )

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
```

### Implementing Query Caching

Now, let's create a simple query caching layer:

```python
# app/models/products.py
import time
from app.models.database import get_db_connection

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
```

### Adding Database Routes to Our Flask App

```python
# Update app/app.py
from app.models.database import init_db
from app.models.products import get_products

# Initialize database on startup
init_db()

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
```

### Create a Products Template

```html
<!-- app/templates/products.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Products - Caching Demo</title>
    <style>
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .pagination { margin: 20px 0; }
        .cache-info { background-color: #f9f9f9; padding: 10px; margin: 10px 0; }
    </style>
</head>
<body>
    <h1>Products List</h1>
    
    <div class="cache-info">
        <p>Query executed in <strong>{{ "%.4f"|format(query_time) }} seconds</strong></p>
        <p>Cache is currently <strong>{{ "ENABLED" if use_cache else "DISABLED" }}</strong></p>
        <p>
            <a href="?cache=true&page={{ pagination.page }}">Enable Cache</a> | 
            <a href="?cache=false&page={{ pagination.page }}">Disable Cache</a>
        </p>
    </div>
    
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Price</th>
            </tr>
        </thead>
        <tbody>
            {% for product in products %}
            <tr>
                <td>{{ product.id }}</td>
                <td>{{ product.name }}</td>
                <td>${{ "%.2f"|format(product.price) }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    
    <div class="pagination">
        {% if pagination.page > 1 %}
            <a href="?page={{ pagination.page - 1 }}&cache={{ 'true' if use_cache else 'false' }}">Previous</a>
        {% endif %}
        
        Page {{ pagination.page }} of {{ pagination.pages }}
        
        {% if pagination.page < pagination.pages %}
            <a href="?page={{ pagination.page + 1 }}&cache={{ 'true' if use_cache else 'false' }}">Next</a>
        {% endif %}
    </div>
</body>
</html>
```

### Exercise 5: Implementing a Cached Product Detail Page

**Objective**: Create a product detail page with caching to improve load times.

1. Add a new function to `app/models/products.py`:

```python
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
```

2. Add a product detail route to `app/app.py`:

```python
from app.models.products import get_product_by_id

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
```

3. Create a product detail template:

```html
<!-- app/templates/product_detail.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{{ product.name }} - Caching Demo</title>
    <style>
        .product-detail { border: 1px solid #ddd; padding: 20px; margin: 20px 0; }
        .cache-info { background-color: #f9f9f9; padding: 10px; margin: 10px 0; }
    </style>
</head>
<body>
    <h1>Product Detail</h1>
    
    <div class="cache-info">
        <p>Query executed in <strong>{{ "%.4f"|format(query_time) }} seconds</strong></p>
        <p>Cache is currently <strong>{{ "ENABLED" if use_cache else "DISABLED" }}</strong></p>
        <p>
            <a href="?cache=true">Enable Cache</a> | 
            <a href="?cache=false">Disable Cache</a>
        </p>
    </div>
    
    <div class="product-detail">
        <h2>{{ product.name }}</h2>
        <p><strong>ID:</strong> {{ product.id }}</p>
        <p><strong>Price:</strong> ${{ "%.2f"|format(product.price) }}</p>
        <p><strong>Description:</strong> {{ product.description }}</p>
        <p><strong>Added:</strong> {{ product.created_at }}</p>
    </div>
    
    <p><a href="/products">Back to Products List</a></p>
</body>
</html>
```

4. Update the products list template to link to detail pages:

```html
<!-- Modify the product row in products.html -->
<td><a href="/products/{{ product.id }}">{{ product.name }}</a></td>
```

5. Test the application by navigating between product pages with caching enabled and disabled to see the performance difference.

## HTTP Caching

HTTP caching leverages standard HTTP headers to instruct browsers and proxy servers on how to cache content.

### Key HTTP Cache Headers

- **Cache-Control**: Specifies caching directives for both requests and responses
- **ETag**: A unique identifier for a specific version of a resource
- **Last-Modified**: Indicates when the resource was last modified
- **Expires**: Provides a date/time after which the response is considered stale
- **Vary**: Specifies which request headers the server uses for selecting a response

### Implementing HTTP Caching in Flask

Let's add HTTP caching to our Flask application:

```python
# Add to app/app.py
from datetime import datetime, timedelta
from flask import make_response, request

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
```

Create the corresponding templates:

```html
<!-- app/templates/static_content.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Static Content - HTTP Caching Demo</title>
</head>
<body>
    {{ content|safe }}
    <p>Refresh the page to test caching. This content should be cached by your browser.</p>
    <p><a href="/">Back to Home</a></p>
</body>
</html>
```

```html
<!-- app/templates/dynamic_content.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Dynamic Content - HTTP Caching Demo</title>
</head>
<body>
    {{ content|safe }}
    <p>Refresh the page to test caching. This content should refresh each time.</p>
    <p><a href="/">Back to Home</a></p>
</body>
</html>
```

```html
<!-- app/templates/conditional_content.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Conditional Content - HTTP Caching Demo</title>
</head>
<body>
    {{ content|safe }}
    <p>Refresh the page to test caching. The server should respond with 304 Not Modified if the content hasn't changed.</p>
    <p><a href="/">Back to Home</a></p>
</body>
</html>
```

### Exercise 6: Analyzing HTTP Caching Behavior

**Objective**: Use browser developer tools to observe HTTP caching behavior.

1. Update the main index page to include links to the caching demo pages:

```html
<!-- Update app/templates/index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Caching Demo</title>
</head>
<body>
    <h1>Caching Workshop</h1>
    
    <h2>Application Features</h2>
    <ul>
        <li><a href="/benchmark">Fibonacci Caching Benchmark</a></li>
        <li><a href="/products">Product List (Database Caching)</a></li>
    </ul>
    
    <h2>HTTP Caching Examples</h2>
    <ul>
        <li><a href="/static-content">Static Content (Long-term Caching)</a></li>
        <li><a href="/dynamic-content">Dynamic Content (No Caching)</a></li>
        <li><a href="/conditional-content">Conditional Content (ETag-based)</a></li>
    </ul>
    
    <div id="data-container">Loading API data...</div>
    
    <script>
        // Simple script to fetch data from our API
        fetch('/api/data')
            .then(response => response.json())
            .then(data => {
                document.getElementById('data-container').innerHTML = 
                    `<pre>${JSON.stringify(data, null, 2)}</pre>`;
            });
    </script>
</body>
</html>
```

2. Open your browser's developer tools (F12 in most browsers).
3. Navigate to the Network tab and check the "Disable cache" option in your browser's developer tools if available, to see the full requests initially.
4. Visit the /static-content page.
* First visit: Observe the HTTP response headers. You should see Cache-Control: public, max-age=3600 and an Expires header. Note the status code (should be 200).
* Refresh the page: Observe the request again. Many browsers will show "200 OK (from disk cache)" or similar, indicating the resource was served from the browser's cache without making a new network request. The request details might show that no actual network request was made to the server for the main HTML document.
5. Visit the /dynamic-content page.
* First visit: Observe the response headers. You should see Cache-Control: no-cache, must-revalidate and a Last-Modified header. Note the status code (200).
* Refresh the page: The browser should make a request back to the server. The server will respond with new content and a 200 status code. The timestamp in the content should update.
6. Visit the /conditional-content page.
* First visit: Observe the response headers. You should see an ETag header (e.g., ETag: "v1-...") and Cache-Control: public, max-age=300. Note the status code (200).
* Refresh the page (within 5 minutes):
* Observe the request headers sent by your browser. It should now include an If-None-Match header with the ETag value from the first response.
* Observe the server's response. It should be a 304 Not Modified status code with an empty body. This tells the browser it can use its cached version.
* Wait for more than 5 minutes (or manually clear the ETag/cache for that specific URL if your browser tools allow) and refresh again. The server should now send a full 200 response with the content because the max-age has expired, forcing a revalidation that might result in new content (though in our simple example, the content is static, so it will be the same, but the ETag mechanism is still demonstrated).

Observations & Questions for You:

* What differences did you notice in the "Size" or "Transferred" column in the Network tab for cached vs. non-cached responses?
* How does the ETag and If-None-Match header combination help save bandwidth?
* Why is Cache-Control: no-cache different from not setting any caching headers at all? (Hint: no-cache still often involves a server check.)

Here's the continuation of your guided learning activity on caching in web applications with Python, maintaining the same structure, tone, and exercise logic:

---

## Implementing Redis for Distributed Caching

### Why Redis for Caching?

Redis (Remote Dictionary Server) is an in-memory data structure store that excels as a distributed cache due to:
- **High performance**: In-memory operations with sub-millisecond latency
- **Persistence options**: Can optionally persist data to disk
- **Rich data structures**: Supports strings, hashes, lists, sets, and more
- **Atomic operations**: Guarantees thread-safe operations
- **Pub/Sub capabilities**: Enables real-time messaging patterns
- **Cluster support**: Horizontal scaling across multiple nodes

### Setting Up Redis

1. Install Redis on your system:
   - **Linux**: `sudo apt-get install redis-server`
   - **MacOS**: `brew install redis`
   - **Windows**: Use the Windows Subsystem for Linux or a Docker container

2. Verify Redis is running:
```bash
redis-cli ping
# Should respond with "PONG"
```

3. Install Python Redis client:
```bash
pip install redis
```

### Basic Redis Caching Example

```python
import redis
import json
import time

# Connect to Redis
cache = redis.Redis(host='localhost', port=6379, db=0)

def get_data_with_redis(key, ttl=60, fallback_function=None):
    """
    Try to get data from Redis cache, falling back to a function if not found
    
    Args:
        key: Cache key
        ttl: Time-to-live in seconds
        fallback_function: Function to call if cache miss occurs
    """
    # Try to get cached data
    cached_data = cache.get(key)
    
    if cached_data is not None:
        print("Cache hit!")
        return json.loads(cached_data)
    
    print("Cache miss!")
    if fallback_function is None:
        return None
    
    # Get data from fallback function
    fresh_data = fallback_function()
    
    # Store in Redis
    cache.setex(key, ttl, json.dumps(fresh_data))
    
    return fresh_data

# Example usage
def fetch_expensive_data():
    """Simulate an expensive operation"""
    time.sleep(2)
    return {"data": "This took a long time to compute", "timestamp": time.time()}

# First call - will be slow (cache miss)
result = get_data_with_redis("expensive_data", 30, fetch_expensive_data)
print(result)

# Second call - will be fast (cache hit)
result = get_data_with_redis("expensive_data", 30, fetch_expensive_data)
print(result)
```

### Exercise 7: Implementing Redis Caching in Flask

**Objective**: Modify our Flask application to use Redis for caching product data.

1. Update `app/app.py` to initialize Redis:

```python
from redis import Redis

# Add to your Flask app configuration
app.config['REDIS_URL'] = 'redis://localhost:6379/0'
redis_client = Redis.from_url(app.config['REDIS_URL'])

# Make redis_client available to other modules
app.extensions['redis'] = redis_client
```

2. Create a new Redis caching module:

```python
# app/utils/redis_cache.py
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
```

3. Update the products model to use Redis:

```python
# app/models/products.py
from app.utils.redis_cache import redis_cache

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
```

4. Add a new route to compare caching methods:

```python
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
```

5. Create a comparison template:

```html
<!-- app/templates/compare_caching.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Caching Comparison</title>
    <style>
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .fastest { background-color: #e6ffe6; }
    </style>
</head>
<body>
    <h1>Caching Method Comparison</h1>
    
    <table>
        <tr>
            <th>Method</th>
            <th>Time (seconds)</th>
            <th>Notes</th>
        </tr>
        <tr class="{{ 'fastest' if redis_time == min([redis_time, memory_time, uncached_time]) }}">
            <td>Redis Caching</td>
            <td>{{ "%.4f"|format(redis_time) }}</td>
            <td>Distributed, survives app restarts</td>
        </tr>
        <tr class="{{ 'fastest' if memory_time == min([redis_time, memory_time, uncached_time]) }}">
            <td>In-Memory Caching</td>
            <td>{{ "%.4f"|format(memory_time) }}</td>
            <td>Simple but app-specific, doesn't scale</td>
        </tr>
        <tr class="{{ 'fastest' if uncached_time == min([redis_time, memory_time, uncached_time]) }}">
            <td>No Caching</td>
            <td>{{ "%.4f"|format(uncached_time) }}</td>
            <td>Always fresh data but slow</td>
        </tr>
    </table>
    
    <p>Page: {{ page }}</p>
    <p>
        <a href="?page={{ page + 1 }}">Next Page</a>
        {% if page > 1 %}
            | <a href="?page={{ page - 1 }}">Previous Page</a>
        {% endif %}
    </p>
    
    <p><a href="/products">Back to Products</a></p>
</body>
</html>
```

### Advanced Redis Patterns

#### Cache Stampede Protection

```python
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
```

#### Redis Pipeline for Batch Operations

```python
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
```

## Cache Invalidation Strategies

### Common Cache Invalidation Patterns

1. **Time-based Expiration (TTL)**
   - Simple to implement
   - Good for data that can be slightly stale
   - Example: `cache.setex(key, 60, value)  # Expires in 60 seconds`

2. **Explicit Invalidation**
   - Delete cache entries when data changes
   - Ensures fresh data but more complex
   - Example: `cache.delete("user:42")`

3. **Write-through Caching**
   - Update cache immediately when data changes
   - Maintains consistency but slower writes

4. **Cache Tags**
   - Group related cache entries
   - Invalidate entire groups when needed
   - Example: Invalidate all "product_*" entries when inventory changes

### Implementing Cache Invalidation

```python
# app/models/products.py
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
```

### Exercise 8: Implementing Cache Invalidation

**Objective**: Create a product update form with proper cache invalidation.

1. Add an update form route to `app/app.py`:

```python
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
```

2. Create an edit product template:

```html
<!-- app/templates/edit_product.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Edit Product</title>
</head>
<body>
    <h1>Edit Product</h1>
    
    <form method="POST">
        <p>
            <label>Name:</label>
            <input type="text" name="name" value="{{ product.name }}" required>
        </p>
        <p>
            <label>Price:</label>
            <input type="number" step="0.01" name="price" value="{{ product.price }}" required>
        </p>
        <p>
            <label>Description:</label>
            <textarea name="description">{{ product.description }}</textarea>
        </p>
        <button type="submit">Update Product</button>
    </form>
    
    <p><a href="/products/{{ product.id }}">Cancel</a></p>
</body>
</html>
```

3. Add a link to the edit page in the product detail template:

```html
<!-- Add to app/templates/product_detail.html -->
<p><a href="/products/{{ product.id }}/edit">Edit Product</a></p>
```

4. Test the implementation:
   - View a product page (notice the cache)
   - Edit the product
   - Verify the changes appear immediately (cache was invalidated)
   - Check the product list to ensure it updates on subsequent views

## Caching in Flask Applications

### Flask-Caching Extension

Flask-Caching provides a simple interface for adding caching to Flask applications.

1. Configure Flask-Caching:

```python
# app/app.py
from flask_caching import Cache

# Configure caching
cache_config = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_REDIS_URL": "redis://localhost:6379/0",
    "CACHE_DEFAULT_TIMEOUT": 300
}
cache = Cache(app, config=cache_config)
```

2. Basic view caching:

```python
@app.route('/expensive-view')
@cache.cached(timeout=60)
def expensive_view():
    time.sleep(3)  # Simulate expensive operation
    return "This view took a long time to generate at: " + str(time.time())
```

3. Memoization for functions:

```python
@cache.memoize(timeout=60)
def expensive_function(param1, param2):
    time.sleep(2)
    return f"Result for {param1} and {param2} at {time.time()}"
```

4. Template fragment caching:

```html
<!-- In your template -->
{% cache 60, "fragment-name" %}
<div>
    This content will be cached for 60 seconds
    Current time: {{ time.time() }}
</div>
{% endcache %}
```

### Exercise 9: Optimizing a Flask API with Caching

**Objective**: Implement caching in a Flask API endpoint.

1. Create a new API endpoint in `app/app.py`:

```python
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
```

2. Create a weather display page:

```python
@app.route('/weather')
def weather_demo():
    return render_template('weather.html')
```

3. Create the weather template:

```html
<!-- app/templates/weather.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Weather Caching Demo</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .container { max-width: 800px; margin: 0 auto; }
        .chart-container { position: relative; height: 300px; }
        .controls { margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Weather API Caching Demo</h1>
        
        <div class="controls">
            <button onclick="fetchWeather(false)">Fetch Fresh Data</button>
            <button onclick="fetchWeather(true)">Use Cached Data</button>
        </div>
        
        <div class="chart-container">
            <canvas id="weatherChart"></canvas>
        </div>
        
        <div id="response"></div>
    </div>
    
    <script>
        const chartCtx = document.getElementById('weatherChart').getContext('2d');
        const weatherChart = new Chart(chartCtx, {
            type: 'line',
            data: { labels: [], datasets: [
                { label: 'Temperature', data: [], borderColor: 'red' },
                { label: 'Response Time', data: [], borderColor: 'blue' }
            ]},
            options: { responsive: true, scales: { y: { beginAtZero: false } } }
        });
        
        let requestCount = 0;
        
        function fetchWeather(useCache) {
            const startTime = performance.now();
            const url = `/api/weather?cached=${useCache}`;
            
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    const responseTime = performance.now() - startTime;
                    
                    // Update chart
                    requestCount++;
                    weatherChart.data.labels.push(requestCount);
                    weatherChart.data.datasets[0].data.push(data.temperature);
                    weatherChart.data.datasets[1].data.push(responseTime);
                    weatherChart.update();
                    
                    // Display response
                    document.getElementById('response').innerHTML = `
                        <pre>${JSON.stringify(data, null, 2)}</pre>
                        <p>Response time: ${responseTime.toFixed(2)}ms</p>
                        <p>Source: ${data.source}</p>
                    `;
                });
        }
        
        // Initial load
        fetchWeather(true);
    </script>
</body>
</html>
```

## Caching in Django Applications

### Setting Up a Django Project

**Note**: If learners already have a Django project set up, they can skip to the caching implementation section.

#### Step 1: Install Django
```bash
pip install django
```

#### Step 2: Create a New Django Project
```bash
django-admin startproject caching_demo
cd caching_demo
```

#### Step 3: Create a Products App
```bash
python manage.py startapp products
```

#### Step 4: Configure the Project

1. Add 'products' to `INSTALLED_APPS` in `caching_demo/settings.py`:
```python
INSTALLED_APPS = [
    ...,
    'products',
]
```

2. Set up the database in `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

3. Configure templates directory in `settings.py`:
```python
TEMPLATES = [
    {
        ...
        'DIRS': [BASE_DIR / 'templates'],
        ...
    },
]
```

#### Step 5: Create Product Model

In `products/models.py`:
```python
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
```

#### Step 6: Make and Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

#### Step 7: Create Superuser
```bash
python manage.py createsuperuser
```

#### Step 8: Register Model in Admin

In `products/admin.py`:
```python
from django.contrib import admin
from .models import Product

admin.site.register(Product)
```

#### Step 9: Add Sample Data

1. Run the development server:
```bash
python manage.py runserver
```

2. Visit http://localhost:8000/admin and add some sample products.

### Implementing Caching in Django

#### Step 1: Configure Cache Backend

In `settings.py`, add Redis cache configuration:
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://localhost:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'django_cache',
    }
}
```

Install required package:
```bash
pip install django-redis
```

#### Step 2: View-Level Caching

In `products/views.py`:
```python
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .models import Product
import time

@cache_page(60 * 5)  # Cache for 5 minutes
def product_list(request):
    start_time = time.time()
    products = Product.objects.all().order_by('name')
    
    # Simulate complex processing
    time.sleep(2)
    
    context = {
        'products': products,
        'execution_time': time.time() - start_time,
    }
    return render(request, 'products/list.html', context)
```

#### Step 3: Create Template

Create `templates/products/list.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Product List</title>
</head>
<body>
    <h1>Product List</h1>
    <p>Generated in {{ execution_time }} seconds</p>
    
    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Price</th>
                <th>Description</th>
            </tr>
        </thead>
        <tbody>
            {% for product in products %}
            <tr>
                <td>{{ product.name }}</td>
                <td>${{ product.price }}</td>
                <td>{{ product.description|truncatewords:10 }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    
    <p><a href="?refresh=1">Force Refresh</a></p>
</body>
</html>
```

#### Step 4: Add URL Pattern

In `caching_demo/urls.py`:
```python
from django.contrib import admin
from django.urls import path
from products.views import product_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', product_list, name='product_list'),
]
```

#### Step 5: Test the View

1. Visit http://localhost:8000/products/
2. Note the loading time on first visit
3. Refresh and note the faster loading time (cached)
4. Add `?refresh=1` to bypass cache

### Template Fragment Caching

Modify `templates/products/list.html`:
```html
{% load cache %}

<!DOCTYPE html>
<html>
<head>
    <title>Product List</title>
</head>
<body>
    <h1>Product List</h1>
    <p>Generated in {{ execution_time }} seconds</p>
    
    {% cache 300 product_table %}  <!-- Cache for 5 minutes -->
    <table>
        <!-- table content same as before -->
    </table>
    {% endcache %}
    
    <p><a href="?refresh=1">Force Refresh</a></p>
</body>
</html>
```

### Low-Level Cache API

#### Step 1: Create a Cached View

In `products/views.py`:
```python
from django.core.cache import cache

def product_detail(request, pk):
    cache_key = f'product_{pk}'
    product = cache.get(cache_key)
    
    if product is None:
        # Simulate slow database query
        time.sleep(2)
        product = Product.objects.get(pk=pk)
        # Cache for 15 minutes
        cache.set(cache_key, product, 60 * 15)
        cache_hit = False
    else:
        cache_hit = True
    
    context = {
        'product': product,
        'cache_hit': cache_hit,
    }
    return render(request, 'products/detail.html', context)
```

#### Step 2: Create Detail Template

Create `templates/products/detail.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ product.name }}</title>
</head>
<body>
    <h1>{{ product.name }}</h1>
    <p>Cache: {% if cache_hit %}HIT{% else %}MISS{% endif %}</p>
    
    <p><strong>Price:</strong> ${{ product.price }}</p>
    <p><strong>Description:</strong> {{ product.description }}</p>
    
    <p><a href="/products/">Back to list</a></p>
</body>
</html>
```

#### Step 3: Add URL Pattern

In `urls.py`:
```python
path('products/<int:pk>/', product_detail, name='product_detail'),
```

### Cache Invalidation

#### Method 1: Using Signals

In `products/models.py`:
```python
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
def invalidate_product_cache(sender, instance, **kwargs):
    cache.delete(f'product_{instance.pk}')
    # Also invalidate list view cache
    cache.delete_pattern('*.views.product_list*')  # Requires django-redis
```

#### Method 2: Manual Invalidation

In `products/views.py`:
```python
from django.http import HttpResponseRedirect

def update_product(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description')
        product.save()
        
        # Manually invalidate cache
        cache.delete(f'product_{pk}')
        return HttpResponseRedirect(f'/products/{pk}/')
    
    return render(request, 'products/update.html', {'product': product})
```

### Exercise 10: Implementing a Cached API

**Objective**: Create a DRF API endpoint with caching.

#### Step 1: Install DRF
```bash
pip install djangorestframework
```

Add to `INSTALLED_APPS`:
```python
'rest_framework',
```

#### Step 2: Create Serializer

In `products/serializers.py`:
```python
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
```

#### Step 3: Create API View

In `products/views.py`:
```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer

@api_view(['GET'])
def product_list_api(request):
    cache_key = 'product_list_api'
    cached_data = cache.get(cache_key)
    
    if cached_data is None:
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        cache.set(cache_key, serializer.data, 60 * 5)  # Cache for 5 minutes
        return Response(serializer.data)
    
    return Response(cached_data)
```

#### Step 4: Add API URL

In `urls.py`:
```python
path('api/products/', product_list_api),
```

#### Step 5: Test the API

1. Visit http://localhost:8000/api/products/
2. Note response time on first request
3. Refresh to see cached response

### Monitoring Django Cache

Install django-debug-toolbar:
```bash
pip install django-debug-toolbar
```

Add to `settings.py`:
```python
INSTALLED_APPS = [
    ...,
    'debug_toolbar',
]

MIDDLEWARE = [
    ...,
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ['127.0.0.1']
```

Add to `urls.py`:
```python
from django.urls import include, path

urlpatterns = [
    ...,
    path('__debug__/', include('debug_toolbar.urls')),
]
```

Now you can see cache operations in the debug toolbar when running in development.



Here's the continuation of your guided learning activity on caching in web applications with Python, maintaining the same structure, tone, and exercise logic:

---

## Implementing Redis for Distributed Caching

### Why Redis for Caching?

Redis (Remote Dictionary Server) is an in-memory data structure store that excels as a distributed cache due to:
- **High performance**: In-memory operations with sub-millisecond latency
- **Persistence options**: Can optionally persist data to disk
- **Rich data structures**: Supports strings, hashes, lists, sets, and more
- **Atomic operations**: Guarantees thread-safe operations
- **Pub/Sub capabilities**: Enables real-time messaging patterns
- **Cluster support**: Horizontal scaling across multiple nodes

### Setting Up Redis

1. Install Redis on your system:
   - **Linux**: `sudo apt-get install redis-server`
   - **MacOS**: `brew install redis`
   - **Windows**: Use the Windows Subsystem for Linux or a Docker container

2. Verify Redis is running:
```bash
redis-cli ping
# Should respond with "PONG"
```

3. Install Python Redis client:
```bash
pip install redis
```

### Basic Redis Caching Example

```python
import redis
import json
import time

# Connect to Redis
cache = redis.Redis(host='localhost', port=6379, db=0)

def get_data_with_redis(key, ttl=60, fallback_function=None):
    """
    Try to get data from Redis cache, falling back to a function if not found
    
    Args:
        key: Cache key
        ttl: Time-to-live in seconds
        fallback_function: Function to call if cache miss occurs
    """
    # Try to get cached data
    cached_data = cache.get(key)
    
    if cached_data is not None:
        print("Cache hit!")
        return json.loads(cached_data)
    
    print("Cache miss!")
    if fallback_function is None:
        return None
    
    # Get data from fallback function
    fresh_data = fallback_function()
    
    # Store in Redis
    cache.setex(key, ttl, json.dumps(fresh_data))
    
    return fresh_data

# Example usage
def fetch_expensive_data():
    """Simulate an expensive operation"""
    time.sleep(2)
    return {"data": "This took a long time to compute", "timestamp": time.time()}

# First call - will be slow (cache miss)
result = get_data_with_redis("expensive_data", 30, fetch_expensive_data)
print(result)

# Second call - will be fast (cache hit)
result = get_data_with_redis("expensive_data", 30, fetch_expensive_data)
print(result)
```

### Exercise 7: Implementing Redis Caching in Flask

**Objective**: Modify our Flask application to use Redis for caching product data.

1. Update `app/app.py` to initialize Redis:

```python
from redis import Redis

# Add to your Flask app configuration
app.config['REDIS_URL'] = 'redis://localhost:6379/0'
redis_client = Redis.from_url(app.config['REDIS_URL'])

# Make redis_client available to other modules
app.extensions['redis'] = redis_client
```

2. Create a new Redis caching module:

```python
# app/utils/redis_cache.py
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
```

3. Update the products model to use Redis:

```python
# app/models/products.py
from app.utils.redis_cache import redis_cache

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
```

4. Add a new route to compare caching methods:

```python
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
```

5. Create a comparison template:

```html
<!-- app/templates/compare_caching.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Caching Comparison</title>
    <style>
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .fastest { background-color: #e6ffe6; }
    </style>
</head>
<body>
    <h1>Caching Method Comparison</h1>
    
    <table>
        <tr>
            <th>Method</th>
            <th>Time (seconds)</th>
            <th>Notes</th>
        </tr>
        <tr class="{{ 'fastest' if redis_time == min([redis_time, memory_time, uncached_time]) }}">
            <td>Redis Caching</td>
            <td>{{ "%.4f"|format(redis_time) }}</td>
            <td>Distributed, survives app restarts</td>
        </tr>
        <tr class="{{ 'fastest' if memory_time == min([redis_time, memory_time, uncached_time]) }}">
            <td>In-Memory Caching</td>
            <td>{{ "%.4f"|format(memory_time) }}</td>
            <td>Simple but app-specific, doesn't scale</td>
        </tr>
        <tr class="{{ 'fastest' if uncached_time == min([redis_time, memory_time, uncached_time]) }}">
            <td>No Caching</td>
            <td>{{ "%.4f"|format(uncached_time) }}</td>
            <td>Always fresh data but slow</td>
        </tr>
    </table>
    
    <p>Page: {{ page }}</p>
    <p>
        <a href="?page={{ page + 1 }}">Next Page</a>
        {% if page > 1 %}
            | <a href="?page={{ page - 1 }}">Previous Page</a>
        {% endif %}
    </p>
    
    <p><a href="/products">Back to Products</a></p>
</body>
</html>
```

### Advanced Redis Patterns

#### Cache Stampede Protection

```python
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
```

#### Redis Pipeline for Batch Operations

```python
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
```

## Cache Invalidation Strategies

### Common Cache Invalidation Patterns

1. **Time-based Expiration (TTL)**
   - Simple to implement
   - Good for data that can be slightly stale
   - Example: `cache.setex(key, 60, value)  # Expires in 60 seconds`

2. **Explicit Invalidation**
   - Delete cache entries when data changes
   - Ensures fresh data but more complex
   - Example: `cache.delete("user:42")`

3. **Write-through Caching**
   - Update cache immediately when data changes
   - Maintains consistency but slower writes

4. **Cache Tags**
   - Group related cache entries
   - Invalidate entire groups when needed
   - Example: Invalidate all "product_*" entries when inventory changes

### Implementing Cache Invalidation

```python
# app/models/products.py
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
```

### Exercise 8: Implementing Cache Invalidation

**Objective**: Create a product update form with proper cache invalidation.

1. Add an update form route to `app/app.py`:

```python
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
```

2. Create an edit product template:

```html
<!-- app/templates/edit_product.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Edit Product</title>
</head>
<body>
    <h1>Edit Product</h1>
    
    <form method="POST">
        <p>
            <label>Name:</label>
            <input type="text" name="name" value="{{ product.name }}" required>
        </p>
        <p>
            <label>Price:</label>
            <input type="number" step="0.01" name="price" value="{{ product.price }}" required>
        </p>
        <p>
            <label>Description:</label>
            <textarea name="description">{{ product.description }}</textarea>
        </p>
        <button type="submit">Update Product</button>
    </form>
    
    <p><a href="/products/{{ product.id }}">Cancel</a></p>
</body>
</html>
```

3. Add a link to the edit page in the product detail template:

```html
<!-- Add to app/templates/product_detail.html -->
<p><a href="/products/{{ product.id }}/edit">Edit Product</a></p>
```

4. Test the implementation:
   - View a product page (notice the cache)
   - Edit the product
   - Verify the changes appear immediately (cache was invalidated)
   - Check the product list to ensure it updates on subsequent views

## Caching in Flask Applications

### Flask-Caching Extension

Flask-Caching provides a simple interface for adding caching to Flask applications.

1. Configure Flask-Caching:

```python
# app/app.py
from flask_caching import Cache

# Configure caching
cache_config = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_REDIS_URL": "redis://localhost:6379/0",
    "CACHE_DEFAULT_TIMEOUT": 300
}
cache = Cache(app, config=cache_config)
```

2. Basic view caching:

```python
@app.route('/expensive-view')
@cache.cached(timeout=60)
def expensive_view():
    time.sleep(3)  # Simulate expensive operation
    return "This view took a long time to generate at: " + str(time.time())
```

3. Memoization for functions:

```python
@cache.memoize(timeout=60)
def expensive_function(param1, param2):
    time.sleep(2)
    return f"Result for {param1} and {param2} at {time.time()}"
```

4. Template fragment caching:

```html
<!-- In your template -->
{% cache 60, "fragment-name" %}
<div>
    This content will be cached for 60 seconds
    Current time: {{ time.time() }}
</div>
{% endcache %}
```

### Exercise 9: Optimizing a Flask API with Caching

**Objective**: Implement caching in a Flask API endpoint.

1. Create a new API endpoint in `app/app.py`:

```python
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
```

2. Create a weather display page:

```python
@app.route('/weather')
def weather_demo():
    return render_template('weather.html')
```

3. Create the weather template:

```html
<!-- app/templates/weather.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Weather Caching Demo</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .container { max-width: 800px; margin: 0 auto; }
        .chart-container { position: relative; height: 300px; }
        .controls { margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Weather API Caching Demo</h1>
        
        <div class="controls">
            <button onclick="fetchWeather(false)">Fetch Fresh Data</button>
            <button onclick="fetchWeather(true)">Use Cached Data</button>
        </div>
        
        <div class="chart-container">
            <canvas id="weatherChart"></canvas>
        </div>
        
        <div id="response"></div>
    </div>
    
    <script>
        const chartCtx = document.getElementById('weatherChart').getContext('2d');
        const weatherChart = new Chart(chartCtx, {
            type: 'line',
            data: { labels: [], datasets: [
                { label: 'Temperature', data: [], borderColor: 'red' },
                { label: 'Response Time', data: [], borderColor: 'blue' }
            ]},
            options: { responsive: true, scales: { y: { beginAtZero: false } } }
        });
        
        let requestCount = 0;
        
        function fetchWeather(useCache) {
            const startTime = performance.now();
            const url = `/api/weather?cached=${useCache}`;
            
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    const responseTime = performance.now() - startTime;
                    
                    // Update chart
                    requestCount++;
                    weatherChart.data.labels.push(requestCount);
                    weatherChart.data.datasets[0].data.push(data.temperature);
                    weatherChart.data.datasets[1].data.push(responseTime);
                    weatherChart.update();
                    
                    // Display response
                    document.getElementById('response').innerHTML = `
                        <pre>${JSON.stringify(data, null, 2)}</pre>
                        <p>Response time: ${responseTime.toFixed(2)}ms</p>
                        <p>Source: ${data.source}</p>
                    `;
                });
        }
        
        // Initial load
        fetchWeather(true);
    </script>
</body>
</html>
```

## Caching in Django Applications

### Django's Cache Framework

Django provides a robust caching framework with multiple backends:

1. Configure caching in `settings.py`:

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://localhost:6379/0',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

2. Per-view caching:

```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache for 15 minutes
def my_view(request):
    # Your view logic
```

3. Template fragment caching:

```html
{% load cache %}
{% cache 500 sidebar %}
    <!-- Sidebar content -->
{% endcache %}
```

4. Low-level cache API:

```python
from django.core.cache import cache

# Set cache
cache.set('my_key', 'my_value', timeout=3600)

# Get cache
value = cache.get('my_key')
```

### Exercise 10: Implementing Caching in Django

**Objective**: Create a cached Django view for product listings.

1. Create a Django view with caching:

```python
# products/views.py
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .models import Product
import time

@cache_page(60 * 5)  # Cache for 5 minutes
def product_list(request):
    start_time = time.time()
    
    # Simulate complex queryset
    products = list(Product.objects.all().order_by('name')[:100])
    
    context = {
        'products': products,
        'execution_time': time.time() - start_time,
        'source': 'cache' if getattr(request, '_cache_update_cache', False) else 'database'
    }
    
    return render(request, 'products/list.html', context)
```

2. Create a template to display the results:

```html
<!-- templates/products/list.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Product List</title>
</head>
<body>
    <h1>Product List</h1>
    <p>Generated in {{ execution_time|floatformat:4 }} seconds (Source: {{ source }})</p>
    
    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Price</th>
            </tr>
        </thead>
        <tbody>
            {% for product in products %}
            <tr>
                <td>{{ product.name }}</td>
                <td>${{ product.price|floatformat:2 }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    
    <p><a href="?refresh=1">Force Refresh</a></p>
</body>
</html>
```

3. Implement cache invalidation on product save:

```python
# products/models.py
from django.db import models
from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

@receiver(post_save, sender=Product)
def clear_product_cache(sender, instance, **kwargs):
    """Clear cache when a product is saved"""
    cache.delete_pattern('*.views.product_list*')  # Requires django-redis
```

## Monitoring and Optimizing Your Cache

### Key Metrics to Monitor

1. **Cache Hit Rate**: Percentage of requests served from cache
2. **Memory Usage**: How much of your cache storage is being used
3. **Eviction Rate**: How often items are being removed due to space constraints
4. **Latency**: Time taken for cache operations
5. **Error Rate**: Failed cache operations

### Redis Monitoring Commands

```bash
# Check Redis memory usage
redis-cli info memory

# Get cache statistics
redis-cli info stats

# Monitor Redis commands in real-time
redis-cli monitor

# Check keyspace information
redis-cli info keyspace
```

### Exercise 11: Analyzing Cache Performance

**Objective**: Create a dashboard to monitor cache performance.

1. Create a monitoring route in `app/app.py`:

```python
@app.route('/cache-stats')
def cache_stats():
    redis_info = redis_client.info()
    
    stats = {
        'memory': {
            'used': redis_info['used_memory_human'],
            'peak': redis_info['used_memory_peak_human'],
            'fragmentation': redis_info['mem_fragmentation_ratio']
        },
        'keys': {
            'total': redis_info['db0']['keys'] if 'db0' in redis_info else 0,
            'expires': redis_info['db0']['expires'] if 'db0' in redis_info else 0
        },
        'hit_rate': {
            'hits': redis_info['keyspace_hits'],
            'misses': redis_info['keyspace_misses'],
            'rate': redis_info['keyspace_hits'] / (redis_info['keyspace_hits'] + redis_info['keyspace_misses']) 
                     if (redis_info['keyspace_hits'] + redis_info['keyspace_misses']) > 0 else 0
        },
        'throughput': {
            'ops_per_sec': redis_info['instantaneous_ops_per_sec']
        }
    }
    
    return render_template('cache_stats.html', stats=stats)
```

2. Create a monitoring template:

```html
<!-- app/templates/cache_stats.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Cache Statistics</title>
    <style>
        .stat-card { border: 1px solid #ddd; padding: 15px; margin: 10px; border-radius: 5px; }
        .stat-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
        .good { color: green; }
        .warning { color: orange; }
        .bad { color: red; }
    </style>
</head>
<body>
    <h1>Cache Statistics</h1>
    
    <div class="stat-grid">
        <div class="stat-card">
            <h2>Memory Usage</h2>
            <p>Used: {{ stats.memory.used }}</p>
            <p>Peak: {{ stats.memory.peak }}</p>
            <p>Fragmentation: 
                <span class="{% if stats.memory.fragmentation < 1.1 %}good{% elif stats.memory.fragmentation < 1.5 %}warning{% else %}bad{% endif %}">
                    {{ "%.2f"|format(stats.memory.fragmentation) }}
                </span>
            </p>
        </div>
        
        <div class="stat-card">
            <h2>Keys</h2>
            <p>Total: {{ stats.keys.total }}</p>
            <p>With TTL: {{ stats.keys.expires }}</p>
        </div>
        
        <div class="stat-card">
            <h2>Hit Rate</h2>
            <p>Hits: {{ stats.hit_rate.hits }}</p>
            <p>Misses: {{ stats.hit_rate.misses }}</p>
            <p>Rate: 
                <span class="{% if stats.hit_rate.rate > 0.8 %}good{% elif stats.hit_rate.rate > 0.5 %}warning{% else %}bad{% endif %}">
                    {{ "%.2f%%"|format(stats.hit_rate.rate * 100) }}
                </span>
            </p>
        </div>
        
        <div class="stat-card">
            <h2>Throughput</h2>
            <p>Operations/sec: {{ stats.throughput.ops_per_sec }}</p>
        </div>
    </div>
    
    <p><a href="/">Back to Home</a></p>
    
    <script>
        // Auto-refresh every 5 seconds
        setTimeout(() => { window.location.reload(); }, 5000);
    </script>
</body>
</html>
```

### Cache Optimization Techniques

1. **Right-sizing your cache**:
   - Monitor memory usage and adjust maxmemory policy
   - Set appropriate TTL values based on data volatility

2. **Key design**:
   - Use consistent naming conventions
   - Avoid overly long keys
   - Consider namespacing (e.g., `user:42:profile`)

3. **Data serialization**:
   - Choose efficient serialization formats (MessagePack, Protocol Buffers)
   - Compress large values

4. **Eviction policies**:
   - Choose appropriate policy (volatile-lru, allkeys-lru, etc.)
   - Monitor eviction rates

## Additional Resources

### Recommended Reading

1. **Books**:
   - "Redis in Action" by Josiah L. Carlson
   - "High Performance Browser Networking" by Ilya Grigorik
   - "Web Scalability for Startup Engineers" by Artur Ejsmont

2. **Online Resources**:
   - [Redis Documentation](https://redis.io/documentation)
   - [HTTP Caching - MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching)
   - [Flask-Caching Documentation](https://flask-caching.readthedocs.io/)
   - [Django Cache Framework](https://docs.djangoproject.com/en/stable/topics/cache/)

### Tools and Libraries

1. **Caching Tools**:
   - [RedisInsight](https://redis.com/redis-enterprise/redis-insight/) - GUI for Redis
   - [Memcached](https://memcached.org/) - Alternative to Redis
   - [Varnish Cache](https://varnish-cache.org/) - HTTP accelerator

2. **Monitoring**:
   - [Grafana](https://grafana.com/) with Redis plugin
   - [Prometheus](https://prometheus.io/) Redis exporter
   - [New Relic](https://newrelic.com/) application monitoring

3. **Python Libraries**:
   - [django-redis](https://github.com/jazzband/django-redis) - Full-featured Redis cache backend for Django
   - [cachetools](https://github.com/tkem/cachetools) - Extensible memoizing collections and decorators
   - [aiocache](https://github.com/aio-libs/aiocache) - Asynchronous caching library

### Final Exercise: Caching Strategy Design

**Objective**: Design a caching strategy for a real-world application.

1. Choose an application you're familiar with (e.g., e-commerce site, blog, social media platform).

2. Document your caching strategy, including:
   - What data/resources to cache
   - Which caching layers to use (browser, CDN, application, database)
   - Cache expiration policies
   - Invalidation strategies
   - Monitoring approach

3. Implement a proof-of-concept for one critical component.

4. Benchmark the performance with and without caching.


This completes the guided learning activity on caching in web applications with Python. You've now explored caching from fundamental concepts through to advanced implementations in both Flask and Django applications. The exercises have provided hands-on experience with different caching strategies and their performance impacts.

Remember that effective caching requires careful consideration of your specific application requirements and data access
