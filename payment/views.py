import json
import random
import string
import logging 
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from . import pesapal_ops3
from django.shortcuts import render, get_object_or_404, redirect
from . import forms
from moontag_app.models import Address, OrderItem, Order

from django.contrib.auth.decorators import login_required
from .utils import get_user_wallet_balance  # Assuming you have a function to get wallet balance
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Sum
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.db import connection
from django.db.models import F
from django.db import transaction, models
from django.views.generic.base import View
from decimal import Decimal
from account.models import Wallet, Transaction



def payment(request):
    account_reference = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    total_cost = 0
    order = None  # Set a default value
    show_more = None  # Set a default value
    if request.method == 'POST':
        form = forms.Payment(request.POST)

        if form.is_valid():
            payment = form.save(commit=False)
            payment.reference = account_reference
            payment.type = 'MERCHANT'
            payment.description = 'product purch'
            Reference = payment.reference
            FirstName = payment.first_name
            LastName = payment.last_name
            Email = payment.email
            PhoneNumber = payment.phone
            Description = payment.description
            Amount = payment.amount
            Type = payment.type
            payment.save()
            iframe_src = pesapal_ops3.post_transaction(Reference, FirstName, LastName, Email, PhoneNumber, Description, Amount, Type)

            print(iframe_src)

            return render(request, 'payment/paynow.html', {'iframe_src': iframe_src})

    else:
        order_id = request.session['order_id']
        order = get_object_or_404(Order, id=order_id)
        total_cost = order.total_amount 
        print(order.total_amount)

        form = forms.Payment()

    addresses = Address.objects.filter(user=request.user)
    
    # Pass order items to the template
    order_items = order.items.all()  # Assuming 'items' is the related name in your Order model
    context = {'amount': total_cost, 'order': order, 'form': form, 'profile': show_more, 'addresses': addresses, 'order_items': order_items}

    return render(request, 'payment/index.html', context)




class PaymentView2(View):
    template_name = 'payment/index1.html'
    model = Wallet

    def get(self, request, deposited_amount):
        # Convert the string to Decimal
        deposited_amount = Decimal(deposited_amount)

        # Use the deposited amount in your context as needed
        context = {'amount': deposited_amount, 'form': DepositForm()}  # Use your actual form

        return render(request, self.template_name, context)

    def post(self, request):
        # Handle the payment logic here

        account_reference = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        total_cost = 0

        form = DepositForm(request.POST)

        if form.is_valid():
            # Your payment logic goes here
            payment = form.save(commit=False)
            payment.user = request.user
            Wallet.reference = account_reference
            Wallet.type = 'MERCHANT'
            Wallet.description = 'product purcha'
            Reference = Wallet.reference
            Description = Wallet.description
            Amount = Wallet.deposited_amount
            Type = Wallet.type
            payment.save()

            # Use pesapal_ops3 to post the transaction and get iframe_src
            iframe_src = pesapal_ops3.post_transaction(Reference, Description, Amount, Type)

            print(iframe_src)


                # Redirect to a success page
            return render(request, 'payment/paynow.html', {'iframe_src': iframe_src})

        context = {'amount': total_cost, 'form': form}
        return render(request, self.template_name, context)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        print(request.body)
        print('POST')
    else:
        params = request.GET
        print(params)
    merchant_reference = params['pesapal_merchant_reference']
    transaction_tracking_id = params['pesapal_transaction_tracking_id']
    print(merchant_reference)
    print(transaction_tracking_id)

    # status = pesapal_ops3.get_detailed_order_status(merchant_reference, transaction_tracking_id)
    status = pesapal_ops3.get_payment_status(merchant_reference, transaction_tracking_id).decode('utf-8')
    p_status = str(status).split('=')[1]

    # Check if pesapal status is COMPLETED
    if p_status == 'COMPLETED':
        # Check if the user has a Wallet
        try:
            wallet = Wallet.objects.get(user=request.user)
        except Wallet.DoesNotExist:
            # If Wallet does not exist, create it
            wallet = Wallet.objects.create(user=request.user)

        # Set payment_done status to True
        wallet.payment_done = True
        wallet.save()

        # Update the balance in the database
        # Assuming the deposited amount is available in the Deposit model
        deposit = Transaction.objects.get(reference=merchant_reference)
        wallet.balance += deposit.deposited_amount
        wallet.save()

        # Add a success message
        messages.success(request, 'Deposit confirmed successfully!')
        
        # Redirect to a success page or return a success response
        return redirect('shop:home')  # Replace 'payment:completed_status' with your actual URL name
    
    # Add a failure message or return a failure response if needed
    messages.error(request, 'Deposit confirmation failed.')
    return HttpResponse(status=400)  # Bad Request





logger = logging.getLogger(__name__)
@login_required
def purchase_via_wallet(request):
    # Retrieve the order from the session
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)

    # Calculate the total price of the order
    total_price = sum(item.total for item in order.items.all())

    # Retrieve the user's wallet balance
    wallet_balance = get_user_wallet_balance(request.user)

    if wallet_balance >= total_price:
        # Sufficient balance in the wallet, proceed with the purchase

        # Create an order and order items
        order.total_amount = total_price
        order.save()

        for item in order.items.all():
            OrderItem.objects.create(
                order=order,
                in_num=f'INV-{order.id}',
                quantity=item.quantity,
                product=item.product,
                price=item.price,
                total=item.total
            )

        # Deduct the purchase amount from the wallet balance
        WalletTransaction.objects.create(
            user=request.user,
            amount=-total_price,
            transaction_type='purchase',
        )

        # Calculate the remaining wallet balance after the purchase
        remaining_balance = get_user_wallet_balance(request.user)

        # Send email to user
        subject = 'Purchase Confirmation'
        message = f'Thank you for your purchase. ${total_price} has been deducted from your wallet. Your remaining balance is ${remaining_balance}.'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [request.user.email]

        send_mail(subject, message, from_email, to_email, fail_silently=False)

        # Clear the cart
        request.session['cartdata'].clear()
        request.session.modified = True

        messages.success(request, 'Purchase successful. Amount deducted from wallet.')
        return HttpResponseRedirect(reverse('payment:purchase_success'))  # Redirect to a success page
    else:
        # Insufficient balance in the wallet
        messages.error(request, 'Insufficient balance in the wallet. Please deposit more funds.')
        return HttpResponseRedirect(reverse('payment:insufficient_balance'))  # Redirect to a page indicating insufficient balance



def purchase_success(request):
    return render(request, 'payment/purchase_success.html')


def insufficient_balance(request):
    return render(request, 'payment/insufficient_balance.html')