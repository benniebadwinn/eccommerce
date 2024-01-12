from django.shortcuts import render, redirect
from account.forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib import messages
import random
from .models import UserOTP,Wallet, Transaction
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.urls import reverse_lazy
from django.urls import reverse
from .forms import UserPublicDetailsForm,DepositForm
from django.http import  HttpResponse, HttpResponseRedirect
# from main.models import Post

from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import SignupForm, LoginUserForm, PasswordChangingForm, EditUserProfileForm, UserPublicDetailsForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
# from main.models import Blog, BlogComment
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserProfuile
from main.models import Blog, BlogComment
from .models import subscriptions
from django.shortcuts import render, redirect,get_object_or_404
from moontag_app.models import ProductAttribute,Product
from django.db.models import Sum

from django.contrib.auth.models import User
from payment.utils import get_user_wallet_balance
import smtplib
from email.message import EmailMessage
from django.views import View
from django.views.generic import (
    
    CreateView, ListView
)
from django.utils.decorators import method_decorator
from decimal import Decimal
import string
from payment import pesapal_ops3

from django.template.loader import render_to_string
from reportlab.lib.pagesizes import letter
import tempfile
from io import BytesIO

from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def generate_pdf(username, balance):
    # Create a BytesIO buffer to receive PDF data
    buffer = BytesIO()

    # Create the PDF object, using BytesIO as its "file"
    p = canvas.Canvas(buffer, pagesize=letter)

    # PDF content generation using ReportLab
    p.drawString(100, 750, f"Username: {username}")
    p.drawString(100, 730, f"Balance: {balance}")

    # More content can be added as needed

    # Close the PDF object cleanly, and we're done
    p.showPage()
    p.save()

    # File buffer to begin from the start
    buffer.seek(0)

    return buffer


def panel(request):
    return render(request, "user/admin_page.html")


class WalletStatementView(ListView):
    model = Transaction
    template_name = 'account/statement.html'
    context_object_name = 'transactions'
    paginate_by = 10  # Adjust the number of transactions per page as needed

    def get_queryset(self):
        # Retrieve all transactions related to the current user's wallet
        user_wallet_transactions = Transaction.objects.filter(wallet__user=self.request.user)

        # You can further customize the queryset based on your requirements

        return user_wallet_transactions

    def get_context_data(self, **kwargs):
        # Call the base implementation to get the original context
        context = super().get_context_data(**kwargs)

        # Fetch the latest Wallet record for the user
        latest_wallet = Wallet.objects.filter(user=self.request.user).latest('transaction_datetime')

        # Retrieve the balance from the latest Wallet record
        balance = latest_wallet.balance

        # Add the balance to the context
        context['balance'] = balance

        return context


@method_decorator(login_required, name='dispatch')
class DepositeView(View):
    template_name = 'payment/deposit.html'
    success_url = 'account:deposit_success'

    def get(self, request):
        form = DepositForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = DepositForm(request.POST)
        if form.is_valid():
            # Convert amount to Decimal
            deposited_amount = Decimal(form.cleaned_data['deposited_amount'])

            # Assuming you have a user object, you can retrieve the wallet associated with the user
            try:
                wallet = Wallet.objects.get(user=request.user)
            except Wallet.DoesNotExist:
                # If the wallet doesn't exist, create a new one
                wallet = Wallet(user=request.user)

            # Set the transaction type
            wallet.transaction_type = 'deposit'

            # Set payment_done to False initially
            wallet.payment_done = False

           

            # Set the deposited_amount field
            wallet.deposited_amount = deposited_amount



            # Save the wallet instance
            wallet.save()

            # Redirect to a payment confirmation page
            return render(request, 'payment/payment_confirmation.html', {'wallet': wallet, 'deposited_amount': deposited_amount})

        # If the form is not valid, render the form again
        return render(request, self.template_name, {'form': form})



def deposit_success(request):
    success_message = messages.get_messages(request)
    return render(request, 'payment/deposit_success.html', {'success_message': success_message})


def is_admin(user):
    return user.is_staff  # Assuming staff users are considered admins




class PaymentView(View):
    template_name = 'payment/index1.html'

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
            deposited_amount = form.cleaned_data['deposited_amount']
            description = 'account deposit'
            type = 'CUSTOMER'
            reference = account_reference

            # Fetch the existing wallet record for the user
            wallet, created = Wallet.objects.get_or_create(user=request.user)

            # Create a new transaction within the wallet
            transaction = wallet.transactions.create(
                transaction_type='deposit',
                description=description,
                type=type,
                reference=reference,
                transaction_amount=deposited_amount,  # Provide a value for transaction_amount
                deposited_amount=deposited_amount,
                
            )

            # Use pesapal_ops3 to post the transaction and get iframe_src
            iframe_src = pesapal_ops3.post_transaction(reference, description, deposited_amount, type)

            print(iframe_src)

            # Redirect to a success page
            return render(request, 'payment/paynow.html', {'iframe_src': iframe_src})

        context = {'amount': total_cost, 'form': form}
        return render(request, self.template_name, context)




@login_required
def wallet_balance(request):
    # Calculate the overall wallet balance
    overall_balance = Wallet.objects.filter(user=request.user).aggregate(Sum('balance'))['balance__sum'] or 0

    # Send email to the user with their overall wallet balance
    subject = 'Wallet Balance Request'
    message = f'Your overall wallet balance is ${overall_balance}.'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [request.user.email]

    send_mail(subject, message, from_email, to_email, fail_silently=False)

    return render(request, 'payment/wallet_balance.html', {'balance': overall_balance})


# 



def logout_view(request):
    """
    Logout
    """
    logout(request)
    messages.success(request, "You are logged out")
    return redirect('/')

def signup(request):
	if request.method == 'POST':
		get_otp = request.POST.get('otp') #213243 #None

		if get_otp:
			get_user = request.POST.get('usr')
			usr = User.objects.get(username=get_user)
			if int(get_otp) == UserOTP.objects.filter(user = usr).last().otp:
				usr.is_active = True
				usr.save()
				messages.success(request, f'Account has been Created For {usr.first_name}')
				return redirect(reverse('account:login'))
				# return redirect('account:login')
			else:
				messages.warning(request, f'You Entered a Wrong OTP')
				return render(request, 'user/login.html', {'otp': True, 'usr': usr})
        # if User.objects.filter(username=username):
        #     messages.error(request, "Username already exist! Try other username")
        #     return redirect('user/signup.html')
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			name = form.cleaned_data.get('name').split(' ')
       
	
			usr = User.objects.get(username=username)
			usr.email = username
			usr.first_name = name[0]
			if len(name) > 1:
				usr.last_name = name[1]
			usr.is_active = False
			usr.save()
			usr_otp = random.randint(100000, 999999)
			UserOTP.objects.create(user = usr, otp = usr_otp)

			mess = f"Hello {usr.first_name},\nYour OTP is {usr_otp}\nThanks!"

			send_mail(
				"Welcome to Badwin - Verify Your Email",
				mess,
				settings.EMAIL_HOST_USER,
				[usr.email],
				fail_silently = False
				)

			return render(request, 'user/signup.html', {'otp': True, 'usr': usr})

		
	else:
		form = SignUpForm()


	return render(request, 'user/signup.html', {'form':form})


def resend_otp(request):
	if request.method == "GET":
		get_usr = request.GET['usr']
		if User.objects.filter(username = get_usr).exists() and not User.objects.get(username = get_usr).is_active:
			usr = User.objects.get(username=get_usr)
			usr_otp = random.randint(100000, 999999)
			UserOTP.objects.create(user = usr, otp = usr_otp)
			mess = f"Hello {usr.first_name},\nYour OTP is {usr_otp}\nThanks!"

			send_mail(
				"Welcome to Badwin - Verify Your Email",
				mess,
				settings.EMAIL_HOST_USER,
				[usr.email],
				fail_silently = False
				)
			return HttpResponse("Resend")

	return HttpResponse("Can't Send ")


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        get_otp = request.POST.get('otp')

        if get_otp:
            get_usr = request.POST.get('usr')
            usr = User.objects.get(username__iexact=get_usr)
            if int(get_otp) == UserOTP.objects.filter(user=usr).last().otp:
                usr.is_active = True
                usr.save()
                login(request, usr)
                return redirect('home')
            else:
                messages.warning(request, 'You Entered a Wrong OTP')
                return render(request, 'user/login.html', {'otp': True, 'usr': usr})

        usrname = request.POST['username']
        passwd = request.POST['password']

        # user = User.objects.filter(username__iexact=usrname).first()
        user = authenticate(request, username=usrname, password=passwd)
        if user is not None:
            login(request, user)
            return redirect('/')
        elif not User.objects.filter(username__iexact=usrname).exists():
            messages.warning(request, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')
            return redirect('account:login')
        elif not User.objects.get(username__iexact=usrname).is_active:
            usr = User.objects.get(username__iexact=usrname)
            usr_otp = random.randint(100000, 999999)
            UserOTP.objects.create(user=usr, otp=usr_otp)
            mess = f"Hello {usr.first_name},\nYour OTP is {usr_otp}\nThanks for shopping with us !"

            send_mail(
                "Welcome to Badwin - Verify Your Email",
                mess,
                settings.EMAIL_HOST_USER,
                [usr.email],
                fail_silently=False
            )
            return render(request, 'user/login.html', {'otp': True, 'usr': usr})
        else:
            messages.warning(request, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')
            return redirect('account:login')

    form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})
    



# @login_required(login_url="/accounts/login/")
def create_profile(request):
    current_user = request.user
    title = "Create Profile"
    if request.method == 'POST':
        form = UserPublicDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.save()
        return HttpResponseRedirect('/')

    else:
        form = UserPublicDetailsForm()
    return render(request, 'user/create_profile.html', {"form": form, "title": title})
            



class profile(LoginRequiredMixin, generic.View):
    model = Blog
    login_url = 'account:login'
    template_name = "authors/profile.html"

    def get(self, request, user_name):
        user_related_data = Blog.objects.filter(author__username=user_name)[:6]
        user_profile_data = UserProfuile.objects.get(user=request.user.id)
        context = {
            "user_related_data": user_related_data,
            'user_profile_data': user_profile_data
        }
        return render(request, self.template_name, context)


@login_required(login_url="/accounts/login/")
def update_profile(request,id):
    user = User.objects.get(id=id)
    profile = Profile.objects.get(user = user)
    form = UpdateProfileForm(instance=profile)
    if request.method == "POST":
            form = UpdateProfileForm(request.POST,request.FILES,instance=profile)
            if form.is_valid():  
                
                profile = form.save(commit=False)
                profile.save()
                return redirect('profile') 
            
    ctx = {"form":form}
    return render(request, 'update_prof.html', ctx)




@login_required
@csrf_exempt
def following(request):
	if request.method == 'POST' and request.user.is_authenticated:
		data = {}
		for usr in request.user.profile.following.all():
			data[usr.id] = {
			 'first_name' : usr.first_name,
			 'last_name': usr.last_name,
			 'username' : usr.username,
			 'pic' : usr.profile.profile_pic.url
			 }
		
		return JsonResponse(data)
	raise Http404()

@login_required
@csrf_exempt
def followers(request):
	if request.method == 'POST' and request.user.is_authenticated:
		data = {}
		for usr in request.user.profile.followers.all():
			data[usr.id] = {
			 'first_name' : usr.first_name,
			 'last_name': usr.last_name,
			 'username' : usr.username,
			 'pic' : usr.profile.profile_pic.url,
			 'followed_back': usr in request.user.profile.following.all()
			 }
		
		return JsonResponse(data)
	raise Http404()

@login_required
def notifications(request):
	noti = Notification.objects.filter(user=request.user, seen = False)
	noti = serializers.serialize('json', noti)
	return JsonResponse({'data':noti})

@login_required
def notifications_seen(request):
	Notification.objects.filter(user=request.user, seen = False).update(seen = True)
	return HttpResponse(True)

@csrf_exempt
@login_required
def clear_notifications(request):
	if request.method == "POST":
		Notification.objects.filter(user=request.user).delete()
		return HttpResponse(True)
	return HttpResponse(False)

def islogin(request):
	return JsonResponse({'is_login':request.user.is_authenticated})







class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangingForm
    login_url = 'account:login'
    success_url = reverse_lazy('password_success')


def password_success(request):
    return render(request, "authors/password_change_success.html")


class UpdateUserView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    form_class = EditUserProfileForm
    login_url = 'account:login'
    template_name = "authors/edit_user_profile.html"
    success_url = reverse_lazy('home')
    success_message = "User updated"

    def get_object(slef):
        return slef.request.user

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR,
                             "Please submit the form carefully")
        return redirect('home')


class DeleteUser(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = User
    login_url = 'account:login'
    template_name = 'authors/delete_user_confirm.html'
    success_message = "User has been deleted"
    success_url = reverse_lazy('home')



	
class UpdatePublicDetails(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    login_url = "account:login"
    form_class = UserPublicDetailsForm
    template_name = "authors/edit_public_details.html"
    success_url = reverse_lazy('home')
    success_message = "User updated"

    def get_object(slef):
        return slef.request.user.userprofuile

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, "Please submit the form carefully")
        return redirect('home')


    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, "Please submit the form carefully")
        return redirect('home')
	


def wishlist(request):
    wishlist_items = Product.objects.filter(users_wishlist=request.user)
    wishlist_count = wishlist_items.count()
    return render(
        request, "account/dashboard/user_wishlist.html", {"wishlist": wishlist_items, "wishlist_count": wishlist_count}
    )


@login_required
def wishlist_product_toggle(request, id):
	
    product = get_object_or_404(Product, pk=id)
    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user)
        messages.success(
            request, product.title + " has been removed from your wishlist"
        )
    else:
        product.users_wishlist.add(request.user)
        messages.success(request, "Added " + product.title + " to your wishlist")
        
    return HttpResponseRedirect(request.META["HTTP_REFERER"])



# subscribe
def subscribe(request):
    try:
        email = request.POST['email']
    except KeyError:
        messages.error(request, "Email not provided.")
        return redirect("/")

    # Assuming the user is authenticated
    if request.user.is_authenticated:
        # Save the subscription with the current user
        subscription = subscriptions(user=request.user, email=email)
        subscription.save()

        messages.success(request, "Subscription Added!")
    else:
        messages.error(request, "User not authenticated. Please log in.")
    
    return redirect("/")





@login_required
def dashboard(request):
    # order_id = request.session.get('order_id', None)
    # order = get_object_or_404(Order, id=order_id)
    return render(request, "account/dashboard/dashboard.html")


def wallet(request):
    return render(request, 'account/wallet.html')