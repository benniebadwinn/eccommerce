from django.shortcuts import redirect, render
from moontag_app.models import Product,Category,Brand,Banner,ProductAttribute,Color,Size,Wishlist,Todo,Withraw,Vendors,VendorAddProduct,OrderItem
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import moontag_project.settings as settings
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str 
from . tokens import generate_token
from django.contrib.auth.decorators import login_required 
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
# from moontag_app.forms import ProductForm, ProductAttributeForm
from django.db.models import Avg ,Sum
import json
from datetime import datetime
import logging
from django.utils.html import strip_tags
from django.core.exceptions import ValidationError











from django.shortcuts import render

from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
# Esoko
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import (
    DetailView,ListView,TemplateView,
    CreateView,UpdateView,DeleteView,ListView,FormView,View
)


from .forms import CartAddProductForm,MpesaNumberForm,VendorForm,OrderCreateForm,CouponForm,NewsletterForm, subscriptions, PickupStationForm,AddressForm,ContactForm,FeedbackForm,ReviewForm
from .models import Category,ProductAttribute,Offer,Cart,CartProduct ,Banner,Product,CouponUsage,Coupon,Wishlist,Order,OrderItem,Address,MpesaPayment,PickupStation,OrderItem,ReviewRating,OfferStatus
# from .cart import Cart
from django.template.loader import render_to_string
from django.db.models import Min, Max
from urllib.parse import unquote
from django.http import HttpResponseRedirect
from django.utils.crypto import get_random_string
from paypal.standard.forms import PayPalPaymentsForm
from .tasks import order_created
from django.http import HttpResponseBadRequest




import datetime as dt
import json
from secrets import compare_digest
import requests
from requests.auth import HTTPBasicAuth
from decimal import Decimal


from django.conf import settings
from django.db.transaction import atomic, non_atomic_requests
from django.http import HttpResponse ,HttpResponseForbidden ,JsonResponse


from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect,get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse
from . mpesa import MpesaAccessToken,LipaNaMpesaPassword
from moontag_app.tasks import order_created
from django.db.models import Avg ,Sum

#stocks
from django.db import transaction
from datetime import datetime, timedelta
import logging
from django.db.models import Count, Avg


from django.views.decorators.http import require_GET
from django.core.mail import send_mail

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import ChatRoom, Message
from account.models import subscriptions  # Add this line
from moontag_app.models import Newsletter


def adminpanel(request):
    return render(request, 'adminpanel/adminpanel.html')



class SendNewsletterView(View):
    template_name = 'newsletter/send_newsletter.html'

    def get(self, request):
        form = NewsletterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = NewsletterForm(request.POST)
        if form.is_valid():
            sender = request.user
            recipients = form.cleaned_data['recipients']

            print(f"Sender: {sender}")
            print(f"Recipients: {recipients}")

            newsletter = form.save(commit=False)
            newsletter.sender = sender
            newsletter.save()

            # Check if any recipients are selected or send_to_all is True
            if recipients or form.cleaned_data['send_to_all']:
                # Send the newsletter using Django's send_mail function
                subject = newsletter.subject
                message = newsletter.content
                recipient_emails = [user.email for user in recipients]

                try:
                    # Sending logic here (modify as per your requirements)
                    if form.cleaned_data['send_to_all']:
                        # Send the newsletter to all subscribers
                        recipient_emails = [subscriber.email for subscriber in subscriptions.objects.all()]
                        send_mail(
                            subject,
                            message,
                            'sender@example.com',  # Replace with your actual sender email
                            recipient_emails,
                            fail_silently=False,
                        )
                    elif recipients:
                        # Send the newsletter to selected recipients
                        send_mail(
                            subject,
                            message,
                            'sender@example.com',  # Replace with your actual sender email
                            recipient_emails,
                            fail_silently=False,
                        )

                    # Mark the newsletter as sent after successfully sending
                    newsletter.sent_at = timezone.now()
                    newsletter.save()

                    # Display success message on the same page
                    messages.success(request, 'Newsletter sent successfully!')
                    return render(request, self.template_name, {'form': NewsletterForm()})

                except Exception as e:
                    print(f"An error occurred while sending the newsletter: {e}")
                    messages.error(request, f'Error sending newsletter. Details: {e}')

            else:
                # Handle the case when no recipients are selected
                print("No recipients selected. The newsletter will not be sent.")
                messages.warning(request, 'No recipients selected. The newsletter will not be sent.')

        return render(request, self.template_name, {'form': form})





def get_chatrooms_with_last_message():
    chat_rooms = ChatRoom.objects.all()
    chat_rooms_with_last_message = []
    
    for room in chat_rooms:
        last_message = Message.objects.filter(chatroom=room).order_by('-timestamp').first()
        
        chat_rooms_with_last_message.append({
            'id': room.id,
            'room_name': room.name,
            'last_message': {
                'message': last_message.message if last_message else None,
                'timestamp': last_message.timestamp if last_message else None,
                'sender': last_message.sender.username if last_message and last_message.sender else None
            }
        })
    
    return chat_rooms_with_last_message

# Create your views here.
def index(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('account:login')
    chat_rooms = get_chatrooms_with_last_message()
    
    return render(request, 'account/index.html', context={'chat_rooms': chat_rooms})

def room(request, room_name):
    chatroom, created = ChatRoom.objects.get_or_create(name=room_name)
    chat_messages = Message.objects.filter(chatroom=chatroom)

    context = {
        'room_name': room_name,
        'chat_messages': chat_messages,
        'current_user': request.user.username
    }

    return render(request, 'account/chat_room.html', context)




def categories(request):
    """
    category list
    """
    category_data = Category.objects.all().order_by('-id')
    return render(request, 'category.html',{'data':category_data})



def brands(request):
    """
    Brands list
    """
    brands_data = Brand.objects.all().order_by('-id')
    return render(request, 'brand.html',{'data':brands_data})



def product_list(request):
    """
    Product list
    """
    product_data = Product.objects.all().order_by('-id')
    return render(request, 'product_list.html',{'data':product_data})



def category_product_list(request,cat_id):
    """
    Product list per category
    """
    category = Category.objects.get(id=cat_id)
    data = Product.objects.filter(category=category).order_by('-id')
    return render(request, 'category_product_list.html',{'data':data})



def brand_product_list(request,brand_id):
    """
    Product list per brand
    """
    brand = Brand.objects.get(id=brand_id)
    data = Product.objects.filter(brand=brand).order_by('-id')
    return render(request, 'category_product_list.html',{'data':data})






def search_result(request):
    """
    Search result for the search box in the header
    """
    q = request.GET['q']
    data = Product.objects.filter(title__icontains=q).order_by('id')
    return render(request,'search_result.html',{'data':data})



def filter_data(request):
    """
    filter for the sidebar in the product list pages that include a sidebar of filters i am using hare also AJAX and JS.
    """
    colors = request.GET.getlist('color[]')
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')
    sizes = request.GET.getlist('size[]')
    minPrice = request.GET['minPrice']
    maxPrice = request.GET['maxPrice']
    all_products = Product.objects.all().order_by('-id').distinct() # becuase product can be in two colors we need put the distinct() function to fach them and dont show the same product that he have the same attribute
    all_products = all_products.filter(productattribute__price__gte=minPrice)
    all_products = all_products.filter(productattribute__price__lte=maxPrice)
    if len(colors) > 0:
        all_products = all_products.filter(productattribute__color__id__in=colors).distinct()
    if len(categories) > 0:
        all_products = all_products.filter(category__id__in=categories).distinct()
    if len(brands) > 0:
        all_products = all_products.filter(brand__id__in=brands).distinct()
    if len(sizes) > 0:
        all_products = all_products.filter(productattribute__size__id__in=sizes).distinct()   
    t = render_to_string('ajax/product-list.html',{'data':all_products})
    return JsonResponse({'data':t})



def add_to_cart(request):
    """
    Add to cart function also with the help of AJAX and JavaScript
    """
    product_id = str(request.GET.get('id'))
    try:
        product_attribute = get_object_or_404(ProductAttribute, id=product_id)
        print(f"Product ID: {product_id}")
        print(f"Product Attribute: {product_attribute}")

        if product_attribute.stock > 0:
            print(f"Stock level: {product_attribute.stock}")

            cart_product = {}
            cart_product[str(request.GET['id'])] = {
                'img': request.GET['img'],
                'title': request.GET['title'],
                'qty': request.GET['qty'],
                'price': request.GET['price'],
            }

            print("Adding to cart...")

            if 'cartdata' in request.session:
                if product_id in request.session['cartdata']:
                    cart_data = request.session['cartdata']
                    cart_data[product_id]['qty']
                    request.session['cartdata'] = cart_data
                else:
                    cart_data = request.session['cartdata']
                    cart_data.update(cart_product)
                    request.session['cartdata'] = cart_data
            else:
                request.session['cartdata'] = cart_product

            print("Cart updated successfully.")

            return JsonResponse({'data': request.session['cartdata'], 'total_items': len(request.session['cartdata'])})
        else:
            error_message = 'Insufficient stock'
            print(f"Error: {error_message}")
            
            return render(request, 'index.html', {'error_message': error_message})
    except ProductAttribute.DoesNotExist:
        error_message = 'Product not found'
        print(f"Error: {error_message}")
        return render(request, 'index.html', {'error_message': error_message})
    





def cart_page(request):
    """
    Cart page with all the things like - total price of all the Products, 
    """
    total_price = 0
    for p_id, item in request.session['cartdata'].items():
        total_price += int(item['qty']) * float(item['price'])
    
    # Assuming you have a default product for related products
    # Modify as needed based on your actual requirements
    product = Product.objects.first()

    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    return render(request, 'cart.html', {
        'cart_data': request.session['cartdata'],
        'total_items': len(request.session['cartdata']),
        'total_price': total_price,
        'related_products': related_products,
    })



def delete_cart_item(request):
    """
    Delete items from cart with help of ajax & java script 
    """
    p_id = str(request.GET['id'])
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            del request.session['cartdata'][p_id]
            request.session['cartdata'] = cart_data
    total_price = 0
    for p_id,item in request.session['cartdata'].items():
        total_price += int(item['qty']) * float(item['price']) # Becuase i change the template with the respone and delete i need to do the same calculate in the new template
    t = render_to_string('ajax/cart_page.html',{'cart_data':request.session['cartdata'],'total_items':len(request.session['cartdata']),'total_price':total_price})
    return JsonResponse({'data':t,'total_items':len(request.session['cartdata'])})



def update_cart_item(request):
    """
    update items from cart with help of ajax & java script 
    """
    p_id = str(request.GET['id'])
    p_qty = request.GET['qty']
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty'] = p_qty
            request.session['cartdata'] = cart_data
    total_price = 0
    for p_id,item in request.session['cartdata'].items():
        total_price += int(item['qty']) * float(item['price']) # Becuase i change the template with the respone and delete i need to do the same calculate in the new template
    t = render_to_string('ajax/cart_page.html',{'cart_data':request.session['cartdata'],'total_items':len(request.session['cartdata']),'total_price':total_price})
    return JsonResponse({'data':t,'total_items':len(request.session['cartdata'])})



@login_required
def checkout(request):
    """
    Checkout page after the Cart page + if someone reach to the page i save it and can check after that if he buy after the checkout
    """
    total_price = 0
    totalPrice = 0
    if 'cartdata' in request.session:
        for p_id,item in request.session['cartdata'].items():
            totalPrice += int(item['qty']) * float(item['price'])
        order = Order.objects.create(user=request.user,total_amt=totalPrice)
        for p_id,item in request.session['cartdata'].items():
            total_price += int(item['qty']) * float(item['price'])
            items = OrderItems.objects.create(order=order,in_num='INV-'+str(order.id),item=item['title'],img=item['img'],qty=item['qty'],price=item['price'],total=float(item['qty'])*float(item['price']))
        host = request.get_host()
        paypal_dict = {'business':settings.PAYPAL_RECIVER_EMAIL,'amount':total_price,'item_name':'OrderNum-'+str(order.id),'invoice':'INV-'+str(order.id),'currency_code':'USD','notify_url':'http://{}{}'.format(host,reverse('paypal-ipn')),'return_url':'http://{}{}'.format(host,reverse('payment_done')),'cancel_return':'http://{}{}'.format(host,reverse('payment_cancelled'))}
        form = PayPalPaymentsForm(initial=paypal_dict)
        return render(request,'checkout.html',{'cart_data':request.session['cartdata'],'total_items':len(request.session['cartdata']),'total_price':total_price,'form':form})



@csrf_exempt
def payment_done(request):
    """
    Payment done Page and View the order detail that you paid
    """
    return_data=request.POST
    order = Order.objects.last()
    order.paid_status = True
    order.save()
    order = Order.objects.last()
    orders = Order.objects.filter(order_dt=order.order_dt)
    return render(request, 'payment-success.html',{'data':return_data,'orders':orders})
	


@csrf_exempt
def payment_canceled(request):
    """
    Payment canceled Page
    """
    return render(request, 'payment-fail.html')



@login_required
def add_product(request):
    """
    Add product
    """
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Product successfully created.")
    form = ProductForm
    return render(request, 'add_product.html',{'form':form})



@login_required
def add_category(request):
    """
    Add Category
    """
    if request.method == "POST" and request.FILES['img']:
        title = request.POST['title']
        img = request.FILES['img']
        category = Category(title=title,img=img)
        category.save()
        messages.success(request, "Your Category successfully created.")
    return render(request,'add_category.html')



@login_required
def add_brand(request):
    """
    Add Brand
    """
    if request.method == "POST" and request.FILES['img']:
        title = request.POST['title']
        img = request.FILES['img']
        brand = Brand(title=title,img=img)
        brand.save()
        messages.success(request, "Your Brand successfully created.")
    return render(request,'add_brand.html')



@login_required
def add_attribute(request):
    """
    Add product attribute - Have to do it if you want show the product properly
    """
    if request.method == "POST" and request.FILES['img']:
        form = ProductAttributeForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Attribute successfully created.")
        else:
            messages.error(request, "Dont saved please check again or try later")
    form = ProductAttributeForm
    return render(request, 'add_attribute.html',{'form':form})



@login_required
def add_color(request):
    """
    Add Color
    """
    if request.method == "POST":
        title = request.POST['title']
        color_code = request.POST['color_code']
        color = Color(title=title,color_code=color_code)
        color.save()
        messages.success(request, "Your Color successfully created.")
    return render(request,'add_color.html')



@login_required
def add_size(request):
    """
    Add Size
    """
    if request.method == "POST":
        title = request.POST['title']
        size = Size(title=title)
        size.save()
        messages.success(request, "Your Size successfully created.")
    return render(request,'add_size.html')



@login_required
def add_banner(request):
    """
    Add Banner
    """
    if request.method == "POST" and request.FILES['img']:
        img = request.FILES['img']
        text = request.POST['text']
        banner = Banner(img=img,text=text)
        banner.save()
        messages.success(request, "Your Banner successfully created.")
    return render(request,'add_banner.html')



def user_dashboard(request):
    """
    User dashboard, he or she can see orders and logout
    """
    return render(request, 'user_dashboard.html')



def user_orders(request):
    """
    After click on the your orders in the dashboard page
    """
    orders = CartOrder.objects.filter(user=request.user,paid_status=True).order_by('-id')
    return render(request, 'user_orders.html',{'orders':orders})



def user_orders_items(request,id):
    """
    You can click in the user order on the order number and fet the items from the order
    """
    order = CartOrder.objects.get(pk=id)
    orders_items = CartOrderItems.objects.filter(order=order).order_by('-id')
    return render(request, 'user_orders_items.html',{'orders_items':orders_items})



def order_search(request):
    """
    Order search in the dashboard Panel / User orders
    """
    q = request.GET['q']
    orders = CartOrder.objects.filter(total_amt=q).order_by('-id')
    return render(request, 'order_search.html',{'orders':orders})
 
    

def checkout_purchasing(request):
    """
    Pepole that get to the checkout page and dont buy + more table with pepole that Buy
    """
    orders = CartOrder.objects.all()
    return render(request, 'checkout_purchasing.html',{'orders':orders})



@login_required
def display_product(request):
    """
    View all the products and Remove option 
    """
    products = Product.objects.all().order_by('-id')
    if request.method == "POST":
        id = request.POST['id']
        product = Product.objects.get(id=id)
        product.delete()
        messages.success(request, 'The product removed')
    return render(request, 'display_product.html',{'products':products})



def data(request):
    """
    Data on the website 
    """
    a = CartOrder.objects.filter(paid_status=True).aggregate(Sum('total_amt'))
    avg = ProductAttribute.objects.aggregate(Avg('price'))
    total_products = Product.objects.all()
    return render(request, 'data.html', {'avg':avg,'total_products':total_products,'total_price':a})



@csrf_exempt
def add_wishlist(request):
    """
    Add To Wishlist Product process
    """
    if request.method == 'POST':
        pid = json.loads(request.body)
        product = Product.objects.get(pk=pid['productId'])
        data = {}
        check_product = Wishlist.objects.filter(product=product,user=request.user).count()
        if check_product > 0:
            data = {
                'bool': False
            }
        else:
            wishliast = Wishlist.objects.create(product=product,user=request.user)
            data = {
                'bool': True
            }
    return JsonResponse(data)



def wishlist(request):
    """
    Wishlist Section
    """
    if request.method == 'POST':
        pid = request.POST['id']
        remove_product = Wishlist.objects.get(product=pid)
        remove_product.delete()
        messages.success(request, 'Removed From Wishlist')
    products = Wishlist.objects.filter(user=request.user).order_by('-id')
    return render(request, 'wishlist.html',{'products':products})



@login_required
def welcome (request):
    """
    Weoclome page React - Username
    """
    user = request.user
    return render(request, 'marketplace/welcome.html', {'user':user})



@login_required
def store_register(request):
    """
    Vendors Register they store
    """
    if request.method == 'POST' and request.FILES['storeImage']:
        store_name = request.POST['storeName']
        company_name = request.POST['companyName']
        store_image = request.FILES['storeImage']
        business_email = request.POST['businessEmail']
        payPal_email = request.POST['payPalEmail']
        if Vendors.objects.filter(store_name=store_name):
                messages.error(request, "Store already exist! Try other Store Name")
                return redirect('home')
        else:
            brand = Brand.objects.create(title=store_name,img=store_image)
            brand.save()
            vendor = Vendors.objects.create(user=request.user,store_name=store_name,company_name=company_name,store_img=store_image,business_email=business_email,pay_pal=payPal_email)
            vendor.save()
            messages.success(request, 'The Store Created')
            return redirect('/store')
    return render(request, 'marketplace/store_register.html')



def store(request):
    """
    Vendor Admin Panel With many of the data
    """
    orders = Order.objects.none()  # Initialize as an empty queryset

    if len(Vendors.objects.filter(user=request.user)) > 0:
        vendor = Vendors.objects.get(user=request.user)
        todos = Todo.objects.filter(user=request.user)
        vendor_products = VendorAddProduct.objects.filter(user=request.user)
        li = []
        for i in vendor_products:
            products = OrderItem.objects.filter(product=i.product).exclude(order__paid=False)
            li.append(products)
        total_sales = Decimal('0')
        for item in li:
            for p in item:
                orders = Order.objects.filter(id=int(p.in_num[4:]))
                total_sales += p.total

        commission_rate = Decimal('0.17')
        after_moontag_commission = total_sales - (total_sales * commission_rate)

        if request.method == 'POST':
            new_task = request.POST['todo']
            save_task = Todo.objects.create(user=request.user, todo=new_task)
            save_task.save()

        return render(request, 'marketplace/index.html', {'user': request.user, 'vendor': vendor, 'products': li,
                                                           'total_sales': total_sales, 'commission': after_moontag_commission,
                                                           'todos': todos, 'orders': orders, 'vendor_products': vendor_products})
    else:
        return redirect('/store-register')





def order_details(request,id):
    """
    Order Details in Vendor Store
    """
    orders = OrderItem.objects.filter(order_id=id)
    return render(request, 'marketplace/orders_detail.html',{'orders':orders})



def delete_todo(request):
    """
    Delete Todo task in Admin marketplace panel
    """
    if request.method == 'POST':
        todo_id = request.POST.get('todoId')
        if todo_id:
            todo = Todo.objects.get(id=todo_id)
            todo.delete()
            return redirect('/store')
        else:
            # Handle the case when 'todoId' is not present in the POST data
            return HttpResponse("Invalid request", status=400)
    else:
        # Handle the case when the request method is not POST
        return HttpResponse("Method not allowed", status=405)
 


def vendor_add_product(request):
    """
    Vendor Add his Products
    """
    user = request.user
    vendor = Vendors.objects.get(user=request.user)
    categories = Category.objects.all()
    brands = Brand.objects.get(title=vendor.store_name)
    colors = Color.objects.all()
    sizes = Size.objects.all()
    if request.method == 'POST':
        title = request.POST['title']
        slug = request.POST['slug']
        
        specs = request.POST['specs']
        category = Category.objects.get(id=request.POST['category'])
        brand = Brand.objects.get(id=request.POST['brand'])
        color =  Color.objects.get(id=request.POST['color']) 
        size = Size.objects.get(id=request.POST['size'])
        product = Product.objects.create(title=title,slug=slug,specs=specs,category=category,brand=brand,is_featured=False)
        product.save()
        new_added_product = Product.objects.last()
        vendor_add_product_model = VendorAddProduct.objects.create(user=request.user,product=new_added_product)
        vendor_add_product_model.save()
        messages.success(request, 'Product Added Succefuly Remamber To add Atribute if you want the product will be displayed on our store')
        return redirect('/store/add-attribute')
    return render(request, 'marketplace/add_product.html', {'user':user,'vendor':vendor,'category':categories,'brand':brands,'colors':colors,'sizes':sizes})



def vendor_add_attribute(request):
    """
    Add Attribute for vendor products
    """
    user = request.user
    vendor = Vendors.objects.get(user=request.user)
    user_brand = Brand.objects.get(title=vendor.store_name)
    products = Product.objects.filter(brand=user_brand.id)
    colors = Color.objects.all()
    sizes = Size.objects.all()
    if request.method == "POST" and request.FILES['img']:
        product = Product.objects.get(id=request.POST['product'])
        color = Color.objects.get(id=request.POST['color'])
        size = Size.objects.get(id=request.POST['size'])
        price = request.POST['price']
        img = request.FILES['img']
        product_attribute = ProductAttribute.objects.create(product=product,color=color,size=size,price=price,img=img)
        product_attribute.save()
        messages.success(request, 'Attribute Added Succefuly')
    return render(request, 'marketplace/add_attribute.html', {'user':user,'vendor':vendor,'products':products,'colors':colors,'sizes':sizes})



def store_products(request):
    """
    Store Products section
    """
    user = request.user
    vendor = Vendors.objects.get(user=request.user)
    products = VendorAddProduct.objects.filter(user=request.user)
    return render(request, 'marketplace/products.html', {'user':user,'vendor':vendor,'products':products})



def vendor_edit_product(request,id):
    """
    Vendor Edit his Products
    """
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        title = request.POST['title']
        slug = request.POST['slug']
        detail = request.POST['detail']
        specs = request.POST['specs']
        Product.objects.filter(id=id).update(title=title,slug=slug,detail=detail,specs=specs)
        return redirect('/store/products')
    return render(request, 'marketplace/edit_product.html', {'product':product})



def withraw(request):
    """
    Vendor Withraw (Get Paid for his sales)
    """
    vendor = Vendors.objects.get(user=request.user)
    vendor_products = VendorAddProduct.objects.filter(user=request.user)
    li = []
    for i in vendor_products:
        products = OrderItem.objects.filter(product=i.product).exclude(order__paid=False)
        li.append(products)
    total_sales = Decimal('0')
    for item in li:
        for p in item:
            total_sales += p.total
    commission_rate = Decimal('0.17')
    after_moontag_commission = total_sales - (total_sales * commission_rate)

    user_withraws = Withraw.objects.filter(user=request.user)
    what_paid = Decimal('0')
    for y in user_withraws:
        what_paid += Decimal(y.amount)
    
    after_moontag_commission -= what_paid

    if request.method == 'POST':
        withraw_request = request.POST['withraw']
        withraw_request_save = Withraw.objects.create(user=request.user, amount=withraw_request)
        withraw_request_save.save()
        return redirect('/store/withraw')

    return render(request, 'marketplace/withraw.html', {'vendor': vendor, 'user': request.user,
                                                        'after_moontag_commission': after_moontag_commission,
                                                        'total_sales': total_sales, 'paid': what_paid})







# hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh










# hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh












# def send_offer_end_email(offer):
#     subject = 'Offer Ended'
#     message = render_to_string('email/offer_end_email.txt', {'offer': offer})
#     from_email = 'your_email@example.com'
#     recipient_list = [offer.recipient_email]  # Change this to the email you want to send to

#     send_mail(subject, message, from_email, recipient_list)



def update_offer_status(request, offer_id):
    try:
        offer = Offer.objects.get(pk=offer_id)
        offer.end_time = timezone.now()  # Set the end time to now
        offer.save()
        return JsonResponse({'success': True})
    except Offer.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Offer not found'})


def home(request, offer_id=None):
    in_wishlist = False
    if request.user.id:
        in_wishlist = ProductAttribute.objects.filter(users_wishlist=request.user).exists()

    # Fetch featured products with associated ProductAttribute and stock level
    featured_products = Product.objects.filter(is_featured=True).order_by('-id')
    for product in featured_products:
        product.product_attribute = ProductAttribute.objects.filter(product=product).first()

    # Fetch top-rated products with associated ProductAttribute and stock level
    top_rated_products = Product.objects.filter(top_rated=True).order_by('-id')
    for product in top_rated_products:
        product.product_attribute = ProductAttribute.objects.filter(product=product).first()

    # Fetch new products with associated ProductAttribute and stock level
    new_products = Product.objects.order_by('-created')[:10]
    for product in new_products:
        product.product_attribute = ProductAttribute.objects.filter(product=product).first()

    # Fetch most visited products with associated ProductAttribute and stock level
    most_visited_products = Product.objects.order_by('-view_count')[:10]
    for product in most_visited_products:
        product.product_attribute = ProductAttribute.objects.filter(product=product).first()

    category_data = Category.objects.all().order_by('-id')
    # sub_category_data = Sub_Category.objects.all().order_by('-id')

    banners = Banner.objects.all().order_by('-id')

    data = Product.objects.filter().order_by('-id')
    data1 = Product.objects.filter(is_data2=True).order_by('-id')
    data3 = Product.objects.filter(is_data3=True).order_by('-id')
    

    # Check if an offer with the same criteria already exists
    existing_offer = Offer.objects.filter(
        title='Example Offer',
        description='This is an example offer.',
        end_time__gte=timezone.now()  # Only get offers with end_time in the future
    ).first()

    # Use the OfferStatus model to track whether the offer has been created
    offer_status, created = OfferStatus.objects.get_or_create()
    if existing_offer or not offer_status.created:
        offer = existing_offer
    else:
        # Only create a new offer if there's no existing offer and it hasn't been created in the OfferStatus model
        offer = Offer.objects.create(
            title='Example Offer',
            description='This is an example offer.',
            end_time=timezone.now() + timezone.timedelta(days=7, hours=5, minutes=30, seconds=15)
        )

        # Set the created field to False to indicate that the offer has been created
        offer_status.created = True
        offer_status.save()

    return render(request, 'index.html', {
        'data': data,
        'data1': data1,
        'data3': data3,
        'banners': banners,
        'offer': offer,
        'in_wishlist': in_wishlist,
        'featured_products': featured_products,
        'top_rated_products': top_rated_products,
        'new_products': new_products,
        'data2': category_data,
        # 'data3': sub_category_data,
        
        'most_visited_products': most_visited_products,
        
    })






def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)




 

# def update_offer_status(request, offer_id):
#     try:
#         offer = Offer.objects.get(pk=offer_id)
#         offer.end_time = timezone.now()  # Set the end time to now
#         offer.save()

#         # Update the offer status in the OfferStatus model
#         offer_status = OfferStatus.objects.first()
#         offer_status.created = False
#         offer_status.save()

#         return JsonResponse({'success': True})
#     except Offer.DoesNotExist:
#         return JsonResponse({'success': False, 'error': 'Offer not found'})









def product_page(request, slug, id):
    if request.method == "POST":
        username = request.POST['username']
        product_name = request.POST['product']
        review_comment = request.POST['comment']
        stars = request.POST['stars']
        review = ProductReview(user=username, product=product_name, review_text=review_comment, review_rating=stars)
        review.save()

    product = Product.objects.get(id=id)

    reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

    related_products = Product.objects.filter(category=product.category).exclude(id=id)[:4]

    in_wishlist = False
    if request.user.id:
        in_wishlist = ProductAttribute.objects.filter(users_wishlist=request.user).exists()

    colors = ProductAttribute.objects.filter(product=product).values('color__id', 'color__title', 'color__color_code').distinct()
    sizes = ProductAttribute.objects.filter(product=product).values('size__id', 'size__title', 'color__id', 'price', 'discountprice').distinct()

    # Fetch the count of reviews for each rating level
    ratings_count = ReviewRating.objects.filter(product=product).values('rating').annotate(count=Count('rating')).order_by('rating')

    # Fetch the average rating for the product
    avg_ratings = ReviewRating.objects.filter(product=product).values('product').annotate(avg=Avg('rating'))

    # Assuming you have the average rating and count information available
    avg_rating = avg_ratings[0]['avg'] if avg_ratings else 0.0
    total_reviews = reviews.count()  # Assuming reviews is a queryset of ReviewRating for the current product

    # Prepare data for rendering in the template
    ratings_count_data = [{'rating': rating['rating'], 'count': rating['count']} for rating in ratings_count]
    percentage_widths = [{'rating': rating['rating'], 'width': rating['count'] / total_reviews * 100} for rating in ratings_count_data]

    return render(request, 'product_page.html', {
        'data': product,
        'ratings_count': ratings_count_data,
        'avg_rating': avg_rating,
        'total_reviews': total_reviews,
        'reviews': reviews,
        'related_products': related_products,
        'in_wishlist': in_wishlist,
        'colors': colors,
        'sizes': sizes,
    })




class ReturnPolicyView(TemplateView):
	template_name = 'return_policy.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Return Policy'
		return context





class ContactView(CreateView):
	template_name = 'contact.html'
	form_class = ContactForm
	success_url = reverse_lazy('contact')

	def form_valid(self, form):
		form.save()
		return super().form_valid(form)

	def form_invalid(self, form):
		return super().form_invalid(form)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Contact Us'
		return context

	def send_mail(self, form):
		subject = form.cleaned_data['subject']
		from_email = form.cleaned_data['from_email']
		if subject and from_email:
			try:
				send_mail(subject, message, from_email, [''])
			except BadHeaderError:
				return HttpResponse('Invalid header found.')


   



class OrderSummaryView( View):
    def get(self, *args, **kwargs):
        orders = Order.objects.filter(user=self.request.user, ordered=False)

        if orders.exists():
            # Get the most recent order if there are multiple (you may adjust this logic)
            order = orders.latest('created')  

            context = {
                'object': order
            }
            return render(self.request, 'cart/detail.html', context)
        else:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")

   



class ManageCartView(View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cp_obj = get_object_or_404(CartProduct, id=cp_id)
        cart_obj = cp_obj.cart

        # Store the previous subtotal before updating the quantity
        prev_subtotal = cp_obj.subtotal

        if action == "inc":
            cp_obj.quantity += 1
        elif action == "dcr":
            cp_obj.quantity = max(1, cp_obj.quantity - 1)
        elif action == "rmv":
            cp_obj.quantity = 0

        cp_obj.subtotal = self.get_subtotal(cp_obj)
        cp_obj.save()

        # Subtract the previous subtotal and add the new one to update the cart total
        cart_obj.total -= prev_subtotal
        cart_obj.total += cp_obj.subtotal
        cart_obj.save()

        # Print details for debugging
        print(f"Action: {action}")
        print(f"Previous Subtotal: ${prev_subtotal}")
        print(f"New Subtotal: ${cp_obj.subtotal}")

        # Redirect to the cart page
        return redirect("shop:mycart")

    def get_subtotal(self, cart_product):
        # Calculate subtotal considering the discounted price if available
        if cart_product.product.discount_price:
            return cart_product.quantity * cart_product.product.discount_price
        else:
            return cart_product.quantity * cart_product.price

import logging




@method_decorator(login_required(login_url='account:login'), name='dispatch')
class OrderCreateView(CreateView):
    model = Order
    form_class = OrderCreateForm
    template_name = 'orders/create.html'
    success_url = reverse_lazy('payment:payment_type')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        print("get_context_data is being called")  # Add this line
        print("User: ", self.request.user)
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        context['cart_data'] = self.request.session.get('cartdata', {})
        logger = logging.getLogger(__name__)
        # Add the following lines to include address object
        address = Address.objects.filter(user=self.request.user).first()
        print("Address: ", address)

        context['address'] = address
        context = {
                'cart_data': self.request.session.get('cartdata', {}),                                                               # A Context is a dictionary with variable names as the key and their values as the value. Hence, if your context for the above template looks like: {myvar1: 101, myvar2: 102}, when you pass this context to the template render method, {{ myvar1 }} would be replaced with 101 and {{ myvar2 }} with 102 in your template. This is a simplistic example, but really a Context object is the context in which the template is being rendered. ref https://stackoverflow.com/questions/20957388/what-is-a-context-in-django
                                                                           # form is set equal to the form variable above
                'couponform': CouponForm(),                                             # This is from forms.py line 39
                                                                          # order is equal to the order definied above
                 'SHOW_COUPON_FORM': True                                                # connected to order_snippet.html
             }
                # Include coupon amount in the context if available
        context['coupon_amount'] = self.request.session.get('coupon_amount', 0)

        # Include order total amount in the context
        order_id = self.request.session.get('order_id')
        if order_id:
            order = get_object_or_404(Order, id=order_id)
            context['order_total_amount'] = order.total_amount

        # Calculate total price from cart_data
        total_price = sum(int(item['qty']) * float(item['price']) for item in self.request.session.get('cartdata', {}).values())
        context['total_price'] = total_price

        return context

    @transaction.atomic
    def form_valid(self, form):
        order = form.save(commit=False)
        order.user = self.request.user
        order.address = Address.objects.filter(user=self.request.user).first()
        pickup_station_id = self.request.session.get('pickup_station')
        if pickup_station_id:
            order.pickup_station = get_object_or_404(PickupStation, id=pickup_station_id)
    
        total_price = sum(int(item['qty']) * float(item['price']) for item in self.request.session.get('cartdata', {}).values())
    
        coupon_code = self.request.session.get('coupon_code')
        coupon_amount = 0
    
        if coupon_code:
            coupon = get_coupon(self.request, coupon_code)
            if coupon:
                coupon_amount = coupon.value
    
        total_amount_before_coupon = total_price
        total_amount_after_coupon = total_price - coupon_amount
    
        order.total_amount = total_amount_after_coupon
        order.save()
    
        for p_id, item in self.request.session.get('cartdata', {}).items():
            product_attribute = get_object_or_404(ProductAttribute, id=p_id)
            quantity_ordered = int(item['qty'])
    
            if product_attribute.stock >= quantity_ordered > 0:
                product_attribute.stock -= quantity_ordered
                product_attribute.save()
    
                OrderItem.objects.create(order=order, in_num='INV-' + str(order.id),
                                         product=item['title'], img=item['img'], quantity=quantity_ordered,
                                         price=item['price'], total=float(quantity_ordered) * float(item['price']))
                
                # Mark the product as ordered
                product_attribute.product.ordered = True
                product_attribute.product.save()
    
            else:
                messages.error(self.request, f"0 stock for product {product_attribute.product.title}. Kindly select another product.")
                return redirect('shop:home')  # Replace 'home' with the actual name or URL pattern for your home page
    
        self.request.session['cartdata'].clear()
        self.request.session.modified = True
        self.request.session['order_id'] = order.id
    
        if 'total_amount' in self.request.session:
            del self.request.session['total_amount']
            self.request.session.modified = True
    
        subject = 'Order Confirmation'
        message = render_to_string('orders/order_confirmation.html', {'order': order})
        plain_message = strip_tags(message)
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [order.user.email]
        send_mail(subject, plain_message, from_email, to_email, html_message=message, fail_silently=False)
    
        return super().form_valid(form)





    def get_success_url(self):
        payment_type = self.request.POST.get('payment_method')
        if payment_type == 'mpesa_on_delivery':
            return reverse_lazy('shop:mpesa_on_delivery')
        elif payment_type == 'pesapal':
            return reverse_lazy('payment:pay')
        elif payment_type == 'paypal':
            return reverse_lazy('payment:purchase_via_wallet')
        elif payment_type == 'wallet':
            return reverse_lazy('payment:purchase_via_wallet')
        else:
            return reverse_lazy('shop:get_mpesa_number')


class PayviaMpesaonDeliveryView(DetailView):
    template_name = 'payments/mpesa_on_delivery.html'
    model = Order  # Specify the model associated with this view

    def get_object(self, queryset=None):
        # Access the session through self.request
        order_id = self.request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        return order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.request.session.get('order_id', None)
        order = get_object_or_404(Order, id=order_id)
        context['order'] = order
        # Include order total amount in the context
        order_id = self.request.session.get('order_id')
        if order_id:
            order = get_object_or_404(Order, id=order_id)
            context['order_total_amount'] = order.total_amount

        # Calculate total price from cart_data
        total_price = sum(int(item['qty']) * float(item['price']) for item in self.request.session.get('cartdata', {}).values())
        context['total_price'] = total_price
        order_items = order.items.all()  # Assuming 'items' is the related name in your Order model

        context.update({
            'amount': order.total_amount,
            'order_items': order_items,
            'order': order,  # Pass order items to the template
        })
        
    
        print("Order Items:")
        if order_items:
            for order_item in order_items:
                print(f"Product: {order_item.product.title}, Quantity: {order_item.quantity}")
        else:
            print("No Order Items found.")
    
        return context

def paypal(request):
        order_id = request.session.get('order_id', None)
        order = get_object_or_404(Order, id=order_id)
        totalPrice = 0
        total_amount = 0
        price = 0
        quantityt = 0
        if 'cartdata' in request.session:
            for item in order.items.all():
                product = item.product
                order_id = request.session.get('order_id', None)
                total_amount = int(order.total_amount())
                order = Order.objects.create(total_amount=total_amount)
                quantity = item.quantity
                item = OrderItem.objects.create(
                    order=order,
                    in_num='INV-' + str(order.id),
                    quantity=item.quantity,
                    product=product,
                    price=item.price,
                    total=quantity * price,
                    total_amount=total_amount
                )

        for item in order.items.all():
            totalPrice = order.total_amount
            exchange_rate_usd_to_ksh = 110.00  # 1 USD to KSH
            exchange_rate_usd_to_ksh = Decimal(str(exchange_rate_usd_to_ksh))

            totalPrice_ksh = order.total_amount
            totalPrice_usd = totalPrice_ksh / exchange_rate_usd_to_ksh
            host = request.get_host()
            paypal_dict = {
                'business': settings.PAYPAL_RECIVER_EMAIL,
                'amount': totalPrice_usd,
                'item_name': 'OrderNum-' + str(order.id),
                'invoice': 'INV-' + str(order.id),
                'currency_code': 'USD',
                'notify_url': 'http://{}{}'.format(host, reverse('shop:paypal-ipn')),
                'return_url': 'http://{}{}'.format(host, reverse('shop:payment_done')),
                'cancel_return': 'http://{}{}'.format(host, reverse('shop:payment_cancelled'))
            }
            form = PayPalPaymentsForm(initial=paypal_dict)
            return render(request, 'checkout.html', {'cart_data': request.session['cartdata'], 'total_items': len(request.session['cartdata']), 'total_price': total_price, 'form': form})




@method_decorator(login_required(login_url='account:login'), name='dispatch')
class CouponAddView(View):
    template_name = 'orders/create.html'

    @transaction.atomic
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)

        if form.is_valid():
            # Step 1: Print statement to check entered coupon code
            code = form.cleaned_data.get('code')
            print(f"Entered Coupon Code: {code}")

            # Step 2: Your logic to retrieve the coupon
            try:
                coupon = Coupon.objects.get(code=code)
                print(f"Retrieved Coupon: {coupon}")
            except Coupon.DoesNotExist:
                coupon = None
                print("Coupon not found in the database.")

            if not coupon:
                messages.error(self.request, "Invalid coupon code. Please try again.")
                return redirect(self.request.META.get('HTTP_REFERER', 'shop:order_create'))

            # Step 3: Check if the coupon has already been used in this session
            if 'coupon_code' in self.request.session and self.request.session['coupon_code'] == coupon.code:
                messages.error(self.request, "Coupon has already been used in this session.")
                return redirect(self.request.META.get('HTTP_REFERER', 'shop:order_create'))

            # Step 4: Check if the coupon is valid (you might have additional validation criteria)
            if not coupon.is_active:
                messages.error(self.request, "Coupon is not active. Please try again.")
                return redirect(self.request.META.get('HTTP_REFERER', 'shop:order_create'))

            discount_amount = coupon.value

            # Apply coupon to cartdata (replace with your logic)
            cartdata = self.request.session.get('cartdata', {})
            for item in cartdata.values():
                if 'total_price' in item:
                    item['total_price'] -= discount_amount * item.get('qty', 0)

            # Store coupon information in the session
            self.request.session['coupon_code'] = coupon.code
            self.request.session['coupon_amount'] = discount_amount
            self.request.session.modified = True

            # Update coupon usage (replace with your logic)
            coupon.used += 1
            coupon.save()

            messages.success(self.request, f"Successfully added coupon '{coupon.code}' with a value of {discount_amount} to cart")

            # Step 5: Print statements for debugging
            print(f"Coupon Code: {coupon.code}")
            print(f"Coupon Amount: {discount_amount}")

            return redirect(self.request.META.get('HTTP_REFERER', 'shop:order_create'))

        else:
            # Handle case where form is not valid (e.g., no code entered)
            messages.error(self.request, "Invalid form submission. Please enter a coupon code.")
            return redirect(self.request.META.get('HTTP_REFERER', 'shop:order_create'))


@csrf_exempt
def payment_done(request):
    """
    Payment done Page and View the order detail that you paid
    """
    return_data=request.POST
    order = Order.objects.last()
    order.paid_status = True
    order.save()
    order = Order.objects.last()
    orders = Order.objects.filter(created=order.created)
    return render(request, 'payment-success.html',{'data':return_data,'orders':orders})




class PaymentCompletedView(LoginRequiredMixin,TemplateView):
    template_name = 'payments/completed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.request.session.get('order_id', None)
        order = get_object_or_404(Order, id=order_id)
        context['order'] = order
        return context

    def get(self, request, *args, **kwargs):
        if 'order_id' in request.session:
            del request.session['order_id']
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'order_id' in request.session:
            del request.session['order_id']
        return super().post(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if 'order_id' not in request.session:
            messages.error(request, 'You have no orders')
            return redirect(reverse('orders:order_list'))
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse('orders:order_list')

        
class PaymentCancelledView(LoginRequiredMixin,TemplateView):
    template_name = 'payments/cancelled.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.request.session.get('order_id', None)
        order = get_object_or_404(Order, id=order_id)
        context['order'] = order
        return context

    def get(self, request, *args, **kwargs):
        if 'order_id' in request.session:
            del request.session['order_id']
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'order_id' in request.session:
            del request.session['order_id']
        return super().post(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if 'order_id' not in request.session:
            messages.error(request, 'You have no orders')
            return redirect(reverse('orders:order_list'))
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse('orders:order_list')





def get_coupon(request, coupon_code):                                                      # This is a coupon function to get coupons and their codes
    try:
        coupon = Coupon.objects.get(code=coupon_code)                                      # From the coupon class, get the code that already exists in the server, and the code attribte should match with the code entered by the user. Remember the function takes in one argument from the user making the request and the other being the code
        return coupon
    except ObjectDoesNotExist:                                                      # If an error is caught after trying the above then the objectdoesnotexist error is given. The base class for Model.DoesNotExist exceptions. A try/except for ObjectDoesNotExist will catch DoesNotExist exceptions for all models. ref https://docs.djangoproject.com/en/3.2/ref/exceptions/
        messages.info(request, "This coupon does not exist")
        return redirect("shop:order_create")


                                                                           # From loginrequired mixin format for decorators ref https://docs.djangoproject.com/en/3.2/topics/auth/default/#the-loginrequired-mixin
def remove_coupon(request):                                                # This is a function to remove a coupon that has been applied                          # this is a function to remove an item from the cart
        try:
            order = Order.objects.get(user=request.user, ordered=False)         # we use get here because coupon is just one thing instead of many. filter will return Queryset.So use get instead of filter. If multiple objects are there use filter, but you need to loop over that queryset to get each objects. ref https://stackoverflow.com/questions/44284850/queryset-object-has-no-attribute This is to get and set the user and ordered fields of the Order class and save them to the 'order' variable
            if order.coupon:
               order.coupon = None                                              # The code to delete the coupon code. ref https://stackoverflow.com/questions/62534452/django-how-to-remove-a-coupon-from-an-order-without-deleting-coupon-from-databa
               order.save()
            
            return redirect("shop:order-summary")

        except ObjectDoesNotExist:                                                      # If an error is caught after trying the above then the objectdoesnotexist error is given. The base class for Model.DoesNotExist exceptions. A try/except for ObjectDoesNotExist will catch DoesNotExist exceptions for all models. ref https://docs.djangoproject.com/en/3.2/ref/exceptions/
            messages.info(request, "This coupon does not exist")
            return redirect("shop:order-summary")                                              # delete the order item




@method_decorator(login_required(login_url='account:login'), name='dispatch')
class OrderListView(LoginRequiredMixin,ListView):
    model = Order
    template_name = 'orders/list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
@method_decorator(login_required(login_url='account:login'), name='dispatch')   
class OrderDetailView(LoginRequiredMixin,DetailView):
    model= Order
    template_name= 'orders/detail.html'
    context_object_name= 'order'
    
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.user != self.request.user:
            raise Http404("Order not found or not accessible.")
        return obj

 
#a view to show list of orders a user has cancelled.
@method_decorator(login_required(login_url='account:login'), name='dispatch')   
class CancelledOrderListView(ListView):
    model= Order
    template_name='orders/cancelled_list.html'

    
    def get_queryset(self):
        return Order.objects.filter(order_status='cancelled',user=self.request.user)
    
    
    
class CancelledOrderDetailView(DetailView):
    model= Order
    template_name='orders/cancelled_detail.html'
    
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.order_status != 'cancelled' or obj.user != self.request.user:
            raise Http404("Order not found or not accessible.")
        return obj
    


    
@method_decorator(login_required(login_url='account:login'), name='dispatch')
class AddressCreateView(CreateView):
    model = Address
    form_class = AddressForm
    template_name = 'users/address_form.html'
    success_url = reverse_lazy('shop:home')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['addresses'] = Address.objects.filter(user=self.request.user)
        return context

    
@method_decorator(login_required(login_url='account:login'), name='dispatch')
class AddressListView(TemplateView):
    template_name = 'users/address_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['addresses'] = Address.objects.filter(user=self.request.user)
        return context



@method_decorator(login_required(login_url='account:login'), name='dispatch')    
class AddressUpdateView(UpdateView):
    model = Address
    form_class = AddressForm
    template_name = 'users/address_form.html'
    success_url = reverse_lazy('shop:address_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['addresses'] = Address.objects.filter(user=self.request.user)
        return context



@method_decorator(login_required(login_url='account:login'), name='dispatch')
class AddressDeleteView(TemplateView):
    template_name = 'users/address_confirm_delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['address'] = Address.objects.get(pk=self.kwargs['pk'])
        return context
    
    def post(self, request, *args, **kwargs):
        address = get_object_or_404(Address, pk=self.kwargs['pk'])
        address.delete()
        return HttpResponseRedirect(reverse('shop:address_list'))



@method_decorator(login_required(login_url='account:login'), name='dispatch')
class AddressDefaultView(TemplateView):
    template_name = 'users/address_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['addresses'] = Address.objects.filter(user=self.request.user)
        return context
    
    def post(self, request, *args, **kwargs):
        address = get_object_or_404(Address, pk=self.kwargs['pk'])
        address.default = True
        address.save()
        return HttpResponseRedirect(reverse('shop:address_list'))
    


def getAccessToken(request):
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    api_URL = settings.MPESA_API_URL

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']

    return HttpResponse(validated_mpesa_access_token)

 

class MpesaNumberView(FormView):
    '''
    a view that renders a form for the user to enter their  mpesa phone number,
    during checkout
    '''
    form_class = MpesaNumberForm
    template_name = 'payments/mpesa_number.html'

    def form_valid(self, form):
        phone_number = form.cleaned_data['phone_number']
        self.request.session['phone_number'] = phone_number
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('shop:lipa_na_mpesa')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.request.session.get('order_id', None)
        order = get_object_or_404(Order, id=order_id)
        context['order'] = order
        return context



@csrf_exempt
@non_atomic_requests
def lipa_na_mpesa(request):
    order_id = request.session['order_id']
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.total_amount
    amount=float(total_cost)
    phone_number = 254728581045
    
    access_token = MpesaAccessToken.validated_mpesa_access_token
    '''
    if not compare_digest(access_token, ''): #we compare the access token to an empty string/invalid token
        return HttpResponseForbidden(
            'Invalid access token. Please generate a new one and try again.',
            content_type='text/plain'
        )
    '''

    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipaNaMpesaPassword.Business_short_code,
        "Password": LipaNaMpesaPassword.decode_password,
        "Timestamp": LipaNaMpesaPassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA":phone_number, 
        "PartyB": LipaNaMpesaPassword.Business_short_code,
        "PhoneNumber":phone_number, 
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "Badwin",
        "TransactionDesc": "Testing stk push"
    }

    response =requests.post(api_url, json=request, headers=headers)
    return JsonResponse(response.json())



@method_decorator(csrf_exempt, name='dispatch')
class MpesaStkPushCallbackView(View):
    def post(self, request):
        data = json.loads(request.body)['Body']['stkCallback']
        
        if data['ResultCode'] == 0:
            # if payment was successful
             try:
                with atomic():
                    MpesaPayment.objects.create(
                        MerchantRequestID=data['MerchantRequestID'],
                        CheckoutRequestID=data['CheckoutRequestID'],
                        ResultCode=data['ResultCode'],
                        ResultDesc=data['ResultDesc'],
                        Amount=data['CallbackMetadata']['Item'][0]['Value'],
                        MpesaReceiptNumber=data['CallbackMetadata']['Item'][1]['Value'],
                        Balance=data['CallbackMetadata']['Item'][2]['Value'],
                        TransactionDate=data['CallbackMetadata']['Item'][3]['Value'],
                        PhoneNumber=data['CallbackMetadata']['Item'][4]['Value'],
                    )
                    order_id = request.session['order_id']
                    order = get_object_or_404(Order, id=order_id)
                    order.paid = True
                    order.save()
                    return redirect(reverse('shop:payment_completed'))
             except IntegrityError:
                return HttpResponse('Payment already exists')

        return JsonResponse({"ResultCode": 0, "ResultDesc": "Success", "ThirdPartyTransID": 0})



@csrf_exempt
def mpesa_webhook(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        #get post data from safaricom and save it to the database
        MpesaPayment.objects.create(
            MerchantRequestID=data['MerchantRequestID'],
            CheckoutRequestID=data['CheckoutRequestID'],
            ResultCode=data['ResultCode'],
            ResultDesc=data['ResultDesc'],
            Amount=data['CallbackMetadata']['Item'][0]['Value'],
            MpesaReceiptNumber=data['CallbackMetadata']['Item'][1]['Value'],
            Balance=data['CallbackMetadata']['Item'][2]['Value'],
            TransactionDate=data['CallbackMetadata']['Item'][3]['Value'],
            PhoneNumber=data['CallbackMetadata']['Item'][4]['Value'],
        )
        #get the order id from the session,and get the order object,then set the order to paid
        order_id = request.session['order_id']
        order = get_object_or_404(Order, id=order_id)
        order.paid = True
        order.save()

        return HttpResponse('success')
    else:
        return HttpResponse('error')
    






@csrf_exempt
def register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipaNaMpesaPassword.Test_c2b_shortcode,
               "ResponseType": "shop:Completed",
               "ConfirmationURL": "https://17c1-197-232-61-217.ngrok-free.app/c2b/v1/ConfirmationURL",
               "ValidationURL": "https://17c1-197-232-61-217.ngrok-free.app/c2b/v1/ValidationURL"}
    response = requests.post(api_url, json=options, headers=headers)

    return HttpResponse(response.text)


@csrf_exempt
def call_back(request):
    pass


@csrf_exempt
def validation(request):

    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))



@csrf_exempt
def confirmation(request):      # we use this function to save successfully transaction in our database.
    mpesa_body = request.body.decode('utf-8')   #  we get the mpesa transaction from the body by decoding using utf-8
    mpesa_payment = json.loads(mpesa_body)    #  we use json.loads method which will assist us to access variables in our request.
    payment = MpesaPayment(
        first_name=mpesa_payment['FirstName'],
        last_name=mpesa_payment['LastName'],
        middle_name=mpesa_payment['MiddleName'],
        description=mpesa_payment['TransID'],
        phone_number=mpesa_payment['MSISDN'],
        amount=mpesa_payment['TransAmount'],
        reference=mpesa_payment['BillRefNumber'],
        organization_balance=mpesa_payment['OrgAccountBalance'],
        type=mpesa_payment['TransactionType'],
    )
    payment.save()
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))




  

class PaymentCompletedView(TemplateView):
    template_name = 'payments/completed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.request.session.get('order_id', None)
        order = get_object_or_404(Order, id=order_id)
        context['order'] = order
        return context

    def get(self, request, *args, **kwargs):
        if 'order_id' in request.session:
            del request.session['order_id']
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'order_id' in request.session:
            del request.session['order_id']
        return super().post(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if 'order_id' not in request.session:
            messages.error(request, 'You have no orders')
            return redirect(reverse('shop:order_list'))
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse('shop:order_list')

        
class PaymentCancelledView(TemplateView):
    template_name = 'payments/cancelled.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.request.session.get('order_id', None)
        order = get_object_or_404(Order, id=order_id)
        context['order'] = order
        return context

    def get(self, request, *args, **kwargs):
        if 'order_id' in request.session:
            del request.session['order_id']
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'order_id' in request.session:
            del request.session['order_id']
        return super().post(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if 'order_id' not in request.session:
            messages.error(request, 'You have no orders')
            return redirect(reverse('shop:order_list'))
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse('shop:order_list')



# moontag funtions
def data(request):
    """
    Data on the website 
    """
    a = Order.objects.filter(paid=True).aggregate(Sum('total_amount'))
    avg = ProductAttribute.objects.aggregate(Avg('price'))
    total_products = Product.objects.all()
    return render(request, 'data.html', {'avg':avg,'total_products':total_products,'total_price':a})



def checkout_purchasing(request):
    """
    Pepole that get to the checkout page and dont buy + more table with pepole that Buy
    """
    orders = Order.objects.all()
    def order_list(request):
         
        orders = Order.objects.all()
    
    return render(request, 'checkout_purchasing.html',{'orders':orders})

def custom_404_page(request,exception):
    return render(request,'404.html', status=40)



# def category_list(request):
#     """
#     category list
#     """
#     category_data = Category.objects.all().order_by('-id')
#     return render(request, 'category.html',{'data':category_data})