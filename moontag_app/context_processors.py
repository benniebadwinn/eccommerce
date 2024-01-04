from .models import Order
from django.shortcuts import render, get_object_or_404, redirect
from moontag_app.models import Wishlist,Product  # Adjust the import based on your actual models

def total_price(request):
    context = {}
    order_id = request.session.get('order_id')
    if order_id:
        order = get_object_or_404(Order, id=order_id)
        context['order_total_amount'] = order.total_amount

    total_price = sum(int(item['qty']) * float(item['price']) for item in request.session.get('cartdata', {}).values())
    context['total_price'] = total_price

    return context



def cart_data(request):
    return {'cart_data': request.session.get('cartdata', {})}





def wishlist_count(request):
    if request.user.is_authenticated:
        wishlist_items = Product.objects.filter(users_wishlist=request.user)
        wishlist_count = wishlist_items.count()
    else:
        wishlist_count = 0

    return {'wishlist_count': wishlist_count}