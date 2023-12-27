from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from account.views import *
# from django.views.generic import RedirectView
from . import views
# from django_registration.backends.one_step.views import RegistrationView


app_name = "account"

urlpatterns = [
	path('signup/', signup, name = 'signup'),
	path('create_profile/', views.create_profile, name='create_profile'),
    path('panel/', views.panel, name ='panel'),
    
    path('login/', login_view, name = 'login'),
    path('update_profile/<int:id>/', views.update_profile, name='update_profile'),
    # path('profile/', views.profile, name='profile'),
	# path('login/', LoginView.as_view(template_name = 'user/login.html', redirect_authenticated_user = True), 
 #    	name = 'login'),
	path('logout/', LogoutView.as_view(next_page = '/'), name = 'logout'),

	path("password-reset/", 
    	PasswordResetView.as_view(template_name='user/password_reset.html'),
    	name="password_reset"),

	path("password-reset/done/", 
		PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), 
		name="password_reset_done"),

	path("password-reset-confirm/<uidb64>/<token>/", 
		PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'), 
		name="password_reset_confirm"),

	path("password-reset-complete/", 
		PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), 
		name="password_reset_complete"),

	path('resendOTP', resend_otp),
	# path('followers', followers),
	# path('following', following),
	# path('notifications', notifications),
	# path('notifications/clear', clear_notifications),
	path('islogin', islogin),

   # Wishlist
    path("wishlist", views.wishlist, name="wishlist"),
    path("add_to_wishlist/<int:id>/", views.wishlist_product_toggle, name="wishlist_product_toggle",),


    path("dashboard/", views.dashboard, name="dashboard"),
    

	
    path('user-profile/<str:user_name>/', views.profile.as_view(), name="profile"),
    path('change_password/', views.PasswordChangeView.as_view(template_name = "authors/password_change.html"), name="change-password"),
    path('password_success/', views.password_success, name="password_success"),
    path('edit_profile/', views.UpdateUserView.as_view(), name="edit_user"),
    path('delete_user/<int:pk>/', views.DeleteUser.as_view(), name="delete_user"),
    path('ushboardpdate_public_details/', views.UpdatePublicDetails.as_view(), name="user_public_details"),
    path('subscribe/', views.Subscribe, name ='subscribe'),
    
    
    
]
