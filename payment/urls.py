from django.urls import path
from . import views
from payment.views import (PaymentView2)

app_name = 'payment'

urlpatterns = [
   
    path('pay/', views.payment, name='pay'),

    path('purchase_via_wallet/', views.purchase_via_wallet, name='purchase_via_wallet'),
    path('purchase_success/', views.purchase_success, name='purchase_success'),
    path('insufficient_balance/', views.insufficient_balance, name='insufficient_balance'),
    path('pay1/<str:deposited_amount>/', PaymentView2.as_view(), name='pay1'),
    path('oauth_callback/', views.callback, name='callback'),
    path('oauth_callback1/', views.callback1, name='callback'),
]