from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse, HttpResponseNotAllowed
from django.contrib import messages

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.total()
    return render(request, 'cart_summary.html', {"cart_products": cart_products, "quantities": quantities, "totals": totals})

def cart_add(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    product_id = request.POST.get('product_id')
    product_qty = request.POST.get('product_qty')
    if not product_id or not product_qty:
        return JsonResponse({'error': 'product_id and product_qty required'}, status=400)
    try:
        product_id = int(product_id)
        product_qty = int(product_qty)
    except ValueError:
        return JsonResponse({'error': 'invalid data'}, status=400)
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.add(product=product, quantity=product_qty)
    cart_item_count = len(cart)
    messages.success(request, "Product added to cart.")
    response = JsonResponse({'qty': cart_item_count})
    return response



def cart_remove(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    product_id = request.POST.get('product_id')
    if not product_id:
        return JsonResponse({'error': 'product_id required'}, status=400)

    try:
        product_id = int(product_id)
    except ValueError:
        return JsonResponse({'error': 'invalid product_id'}, status=400)

    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.remove(product=product)
    cart_item_count = len(cart)
    totals = cart.total()
    response = JsonResponse({'qty': cart_item_count, 'total': totals})
    messages.success(request, "Product removed from cart.")
    return response

def cart_update(request):
    cart = Cart(request)
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    product_id = request.POST.get('product_id')
    product_qty = request.POST.get('product_qty')
    if not product_id or not product_qty:
        return JsonResponse({'error': 'product_id and product_qty required'}, status=400)
    try:
        product_id = int(product_id)
        product_qty = int(product_qty)
    except ValueError:
        return JsonResponse({'error': 'invalid data'}, status=400)
    
    cart.update(product=product_id, quantity=product_qty)
    response = JsonResponse({'qty':product_qty})
    messages.success(request, "Cart updated successfully.")
    return response
