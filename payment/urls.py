from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('home', views.home, name='home'),
    path('payment/', views.payment, name='pay'),
    path('purchase_via_wallet/', views.purchase_via_wallet, name='purchase_via_wallet'),
    path('purchase_success/', views.purchase_success, name='purchase_success'),
    path('insufficient_balance/', views.insufficient_balance, name='insufficient_balance'),
    path('payment/oauth_callback/', views.callback, name='callback'),
]