from django.urls import path,include
from moontag_app import views
from django.conf import settings
from django.conf.urls.static import static
from moontag_app.views import (ManageCartView,MpesaStkPushCallbackView,MpesaNumberView,
    PayviaMpesaonDeliveryView,PaymentCompletedView,
     PaymentCancelledView,AddressCreateView,SendNewsletterView,AddressListView,AddressUpdateView, AddressDeleteView,CouponAddView,remove_coupon,CouponAddView,OrderListView,OrderSummaryView,)
# from moontag_app.consumers import ChatConsumer


# from moontag_app.views import (AddressCreateView,OrderSummaryView,AddressListView,AddressUpdateView, AddressDeleteView,MpesaStkPushCallbackView,MpesaNumberView,
#     PayviaMpesaonDeliveryView,PaymentCompletedView,
#     PaymentCancelledView,OrderCreateView,EmptyCartView,MyCartView,ManageCartView,CouponAddView,remove_coupon,CouponAddView,add_to_cart)




app_name = 'shop'


urlpatterns = [
    path('',views.home,name='home'),

    path('categories',views.categories,name='categories'),
    path('brands',views.brands,name='brands'),
    path('product-list',views.product_list,name='product-list'),
    path('category-product-list/<int:cat_id>',views.category_product_list,name='category-product-list'),
    path('brand-product-list/<int:brand_id>',views.brand_product_list,name='brand-product-list'),
    path('product/<str:slug>/<int:id>',views.product_page,name='product_page'),
    path('search-result',views.search_result,name='search_result'),
    path('filter-data',views.filter_data,name='filter_data'),
    path('add-to-cart',views.add_to_cart,name='add_to_cart'),
    
    path('delete-from-cart',views.delete_cart_item,name='delete_cart_item'),
    path('update-cart',views.update_cart_item,name='update-cart'),
    path('checkout',views.checkout,name='checkout'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
    path('add-product',views.add_product,name='add_product'),
    path('add-category',views.add_category,name='add_category'),
    path('add-brand',views.add_brand,name='add_brand'),
    path('add-color',views.add_color,name='add_color'),
    path('add-size',views.add_size,name='add_size'),
    path('add-banner',views.add_banner,name='add_banner'),
    path('user-dashboard',views.user_dashboard,name='user_dashboard'),
    path('user-orders',views.user_orders,name='user_orders'),
    path('user-orders-items/<int:id>',views.user_orders_items,name='user_orders_items'),
    path('add-attribute',views.add_attribute,name='add_attribute'),
    path('order-search',views.order_search,name='order_search'),
    path('checkout-purchasing',views.checkout_purchasing,name='checkout_purchasing'),
    path('display-product',views.display_product,name='display_product'),
    path('data',views.data,name='data'),
    path('add-wishlist',views.add_wishlist,name='add_wishlist'),
    path('wishlist',views.wishlist,name='wishlist'),
    path('store-register',views.store_register,name='store_register'),
    path('welcome',views.welcome,name='welcome'),
    path('store',views.store,name='store'),
    path('store/add-product',views.vendor_add_product,name='vendor_add_product'),
    path('store/add-attribute',views.vendor_add_attribute,name='vendor_add_attribute'),
    path('store/todo/delete',views.delete_todo,name='delete_todo'),
    path('store/order/<int:id>',views.order_details,name='order_details'),
    path('store/products',views.store_products,name='store_products'),
    path('store/products/edit/<int:id>',views.vendor_edit_product,name='vendor_edit_product'),
    path('store/withraw',views.withraw,name='withraw'),
















        
    # path('',views.home,name='home'),
    
    # path('product-list',views.product_list,name='product-list'),
    # path('filter-data',views.filter_data,name='filter_data'),
   
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    
   
    # # path('cart_detail/', OrderSummaryView.as_view(), name='cart_detail'), 
    # path('wishlist', views.WishlistView.as_view(), name='wishlist'),
    # path('wishlist/add/<int:id>/', views.AddToWishlistView.as_view(), name='wishlist_add'),
    # path('wishlist/remove/<int:id>/', views.RemoveFromWishlistView.as_view(), name='wishlist_remove'),
    
    # path('coupon-list/', views.CouponListView.as_view(), name='coupon_list'),
    # # path('product-page/<int:id>/<slug:slug>/', ProductDetailView.as_view(), name='product-page'), 
    # path('product/<str:slug>/<int:id>',views.product_page,name='product_page'),    # the slug, and "as_view" and name are as per the format giving by Django for using the "Detail view". It is required. Ref: https://docs.djangoproject.com/en/3.2/ref/class-based-views/generic-display/#detailview)
    
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
    # path('create/', views.ProductCreateView.as_view(), name='product_create'),
    # # path('add-to-my-cart/<slug:slug>>/', addition_to_cart, name='add-to-cart'),               # This is in connection to the addition_to_cart function in the views.py
    path('add-coupon/', CouponAddView.as_view(), name='add-coupon'),                   
    # # path('remove-from-cart/<slug>/', remove_item_from_cart, name='remove-from-cart'),   # This is in connection to the remove_item_from_cart function in the views.py
    path('remove-coupon/', remove_coupon, name='remove-coupon'),                        # This is in connection to the remove_item_from_cart function in the views.py
    # # path('remove-item-from-cart/<slug>/', remove_one_item_from_cart, name='remove-one-item-from-cart'),    # This is in connection to the remove_one_item_from_cart function in the views.py
    # path('delivery_method', views.ConfirmShippingAddressView.as_view(), name='delivery_method'),
    # path('Newsletter', views.NewsLetterView.as_view(), name='Newsletter'),
    path('list', views.OrderListView.as_view(), name='my_orders'),
    path('list-cancelled', views.CancelledOrderListView.as_view(), name='cancelled_orders'),
    path('cancelled-detail/<int:pk>/', views.CancelledOrderDetailView.as_view(),name='cancelled_order_detail'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),


    # #users
    #path('profile/', views.profile, name='profile'),
    path('address/create/', AddressCreateView.as_view(), name='address_create'),
    path('address/update/<int:pk>/', AddressUpdateView.as_view(), name='address_update'),
    path('address/delete/<int:pk>/', AddressDeleteView.as_view(), name='address_delete'),
    path('address/list/', AddressListView.as_view(), name='address_list'),



    path('access/token', views.getAccessToken, name='get_mpesa_access_token'),
    path('c2b/register/', views.register_urls, name="register_mpesa_validation"),
    path('c2b/confirmation', views.confirmation, name="confirmation"),
    path('c2b/validation/', views.validation, name="validation"),
    
    path('mpesa_number',MpesaNumberView.as_view(),name='get_mpesa_number'),

    path('lipa-na-mpesa', views.lipa_na_mpesa, name='lipa_na_mpesa'),
    path('mpesa-webhook', views.mpesa_webhook, name='mpesa_webhook'),
    path('stk-push/callback', MpesaStkPushCallbackView.as_view(), name='mpesa-stk-push-callback'),
    path('mpesa-on-deliverly', PayviaMpesaonDeliveryView.as_view(), name='mpesa_on_delivery'),
    # path('bank-transfer/', BankTransferView.as_view(), name='bank_transfer'),
    path('completed', PaymentCompletedView.as_view(), name='completed'),
    path('cancelled', PaymentCancelledView.as_view(), name='cancelled'),
    # path('search-result',views.search_result,name='search_result'),
    # path('filter-data',views.filter_data,name='filter_data'),
    # # moontag functions
    # path('data/',views.data,name='data'),
    # path('checkout-purchasing',views.checkout_purchasing,name='checkout_purchasing'),
    # # path('product-list',views.product_list,name='product-list'),

    # # path('category-product-list/<int:cat_id>',views.category_product_list,name='category-product-list'),
    # path('categories/', views.category_list, name='category_list'),

    path('update_offer_status/<int:offer_id>/', views.home, name='update_offer_status'),


    
    path("manage-cart/<int:cp_id>/", ManageCartView.as_view(), name="managecart"),
    # # path("my-cart/", MyCartView.as_view(), name="mycart"),
    path('cart',views.cart_page,name='cart'),
    # path('empty-cart/', EmptyCartView.as_view(), name='emptycart'),
    # # path("add-to-cart-<int:product_id>/", AddToCartView.as_view(), name="add-to-cart"),
    # path('add-to-cart',views.add_to_cart,name='add_to_cart'),
    path('paypal/', views.paypal, name='paypal'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('completed/', PaymentCompletedView.as_view(), name='completed'),
    path('cancelled/', PaymentCancelledView.as_view(), name='payment_cancelled'),
    path('custom_404_page/', views.custom_404_page , name='custom_404_page'),
    
    
    path('livechat/', views.index, name='index'),
    path('adminpanel/', views.adminpanel, name='adminpanel'),
    path('chat/<str:room_name>/', views.room, name='room'),
    path('send/', SendNewsletterView.as_view(), name='send_newsletter'),
   
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)