from django import forms
from moontag_app.models import Product, ProductAttribute



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['slug','detail','specs','category','brand','status','is_featured']


# class ProductAttributeForm(forms.ModelForm):
#     class Meta:
#         model = ProductAttribute
#         fields = ['product','color','size','price','img']








from django import forms

from .models import Vendor,Wishlist,Order,CouponUsage,Contact,Feedback,ReviewRating,Product,CartProduct,Coupon

from django.utils.translation import gettext_lazy as _
# from account.forms import SignupForm
#from users.models import Address,PickupStation
from account.models import *
from django.contrib.auth import get_user_model
from django.forms import HiddenInput



PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


# class CartAddProductForm(forms.Form):
#     quantity = forms.TypedChoiceField(
#                                 choices=PRODUCT_QUANTITY_CHOICES,
#                                 coerce=int)
#     override = forms.BooleanField(required=False,
#                                   initial=False,
#                                   widget=forms.HiddenInput)




class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)




class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ('name', 'phone_number', 'email', 'location', 'description', 'image', 'owner')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['location'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        self.fields['owner'].widget.attrs.update({'class': 'form-control'})

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError('This field is required')
        return name

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number:
            raise forms.ValidationError('This field is required')
        return phone_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('This field is required')
        return email


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']




#a form for adding a product to wishlist
class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ('product', 'user')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].widget.attrs.update({'class': 'form-control'})
        self.fields['user'].widget.attrs.update({'class': 'form-control'})

    def clean_product(self):
        product = self.cleaned_data.get('product')
        if not product:
            raise forms.ValidationError('This field is required')
        return product

    def clean_user(self):
        user = self.cleaned_data.get('user')
        if not user:
            raise forms.ValidationError('This field is required')
        return user
    



class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={                       # A string field, for small- to large-sized strings. ref https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/
        'class': 'form-control',                                                 # These lines are from order_snippet.html line 37                                 # On a real Web page, you probably don’t want every widget to look the same. You might want a larger input element for the comment, and you might want the ‘name’ widget to have some special CSS class. It is also possible to specify the ‘type’ attribute to take advantage of the new HTML5 input types. To do this, you use the Widget.attrs argument when creating the widget. In this case we manipulated the placeholder attribute. ref https://docs.djangoproject.com/en/3.2/ref/forms/widgets/#django.forms.Widget.attrs
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))




class CartProductForm(forms.ModelForm):
    class Meta:
        model = CartProduct
        fields = ['product', 'quantity']
    

    class Meta:
        model = Order
        fields = ['payment_method', 'coupon']
        labels = {
            'coupon': _('Coupon'),
            'payment_method': _('Payment Method'),
        }


    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        #self.fields['coupon'].queryset = Coupon.objects.filter(is_active=True).exclude(is_active=False)
           
  

class AddressForm(forms.ModelForm):
   
    class Meta:
        model = Address
        fields = [
            'address_name','region','phone_number','additional_phone_number',
            'delivery_instructions','default_address'
            ]

#form to select a pickup station
from django import forms
from django.forms.widgets import HiddenInput
from .models import PickupStation  # Replace with the actual import for PickupStation

class PickupStationForm(forms.Form):
    PICKUP_CHOICES = [
        ('Dropped at a Pickup Station', 'Dropped at a Pickup Station'),
        ('Home / Office Delivery', 'Home / Office Delivery'),
    ]

    pickup_option = forms.ChoiceField(
        choices=PICKUP_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        required=True,
        initial='Pickup Station',
    )

    pickup_station = forms.ModelChoiceField(
        queryset=PickupStation.objects.all(),
        required=False,
        empty_label='Select a pickup station',
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
    )

    pickup_station_hidden = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PickupStationForm, self).__init__(*args, **kwargs)

        # Set the initial value for the pickup_station_hidden field based on the request
        initial_option = self.initial.get('pickup_option')
        if initial_option:
            self.fields['pickup_option'].initial = initial_option
            self.fields['pickup_station_hidden'].initial = self.get_default_pickup_station_id()

    def get_default_pickup_station_id(self):
        # Implement this method to return the ID of the default pickup station based on your logic.
        # For example, you might retrieve the default pickup station from the user's profile.
        # This method should return None if there is no default pickup station.
        return None







class OrderCreateForm(forms.ModelForm):
    PAYMENT_METHOD_CHOICES = [
        ('mpesa_on_delivery', 'Mpesa on Delivery'),
        ('mpesa', 'Mpesa'),
        ('pesapal', 'Pesapal'),
        ('wallet', 'Wallet'),
        ('paypal', 'Paypal'),
    ]

    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        required=True,
        initial='Mpesa on Delivery',  # Set the initial value to 'mpesa' or any other value you prefer
    )

    # Add a hidden input for payment_method
    payment_method_hidden = forms.CharField(widget=HiddenInput(), required=False)

    class Meta:
        model = Order
        fields = ['payment_method', 'coupon']
        labels = {
            'coupon': _('Coupon'),
            'payment_method': _('Payment Method'),
        }
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'coupon': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(OrderCreateForm, self).__init__(*args, **kwargs)


class MpesaNumberForm(forms.Form):
    phone_number=forms.IntegerField(
        widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'2547xxxxxxxx'})
        
        
    )


   

# Create your forms here.

class ContactForm(forms.ModelForm):
	class Meta:
		model = Contact
		fields = ['first_name', 'last_name', 'email_address', 'message']


class FeedbackForm(forms.ModelForm):
	class Meta:
		model = Feedback
		fields = ['name', 'feedback', 'email']




# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ['name','slug','description','category','is_featured']


