from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .models import Product
import time
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer
from django.core.cache import cache

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