from moontag_app.models import Product,ProductAttribute
from django.db.models import Min,Max
from .models import Order

def get_filters(request):
    category = Product.objects.distinct().values('category__title','category__id')
    brands = Product.objects.distinct().values('brand__title','brand__id')
    colors = ProductAttribute.objects.distinct().values('color__title','color__id','color__color_code')
    sizes = ProductAttribute.objects.distinct().values('size__title','size__id')
    max_min_price = ProductAttribute.objects.aggregate(Min('price'),Max('price'))
    data = {'category':category,'brands':brands,'colors':colors,'sizes':sizes,'max_min_price':max_min_price}
    return data





def total_price(request):
    context = {}
    order_id = request.session.get('order_id')
    if order_id:
        order = get_object_or_404(Order, id=order_id)
        context['order_total_amount'] = order.total_amount

    total_price = sum(int(item['qty']) * float(item['price']) for item in request.session.get('cartdata', {}).values())
    context['total_price'] = total_price

    return context