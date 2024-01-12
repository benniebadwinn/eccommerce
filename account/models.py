from django.db import models
from django.contrib.auth.models import User
from PIL import Image


from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model  # current user model
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

User = get_user_model()



class UserOTP(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	time_st = models.DateTimeField(auto_now = True)
	otp = models.SmallIntegerField()

def upload_profile_to(instance,filename):
	return f'profile_picture/{instance.user.username}/{filename}'

def upload_cover_to(instance,filename):
	return f'coverImage/{instance.user.username}/{filename}'


class UserProfuile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=50, blank=True)
    dob = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to="media/product_images", blank=True)
    currently_learning = models.TextField(blank=True)
    skills_language = models.TextField(blank=True)
    currently_hacking_on = models.TextField(blank=True)
    website = models.URLField(blank=True)
    github = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    education = models.TextField(blank=True)
    work = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
	

class subscriptions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()

    def __str__(self):
        return self.user.username 



GENDER_CHOICES = (
    ('male', 'Male'),
    ('female','Female'),
    ('other', 'Other'))

REGIONS = (
        ('Nairobi',(
            ('Nairobi Central','Nairobi Central'),
            ('Nairobi CBD','Nairobi CBD'),
            ),
            ),
        ('Nakuru',(
            ('Nakuru Central','Nakuru Central'),
            ('Nakuru CBD','Nakuru CBD'),
            ),
        ),
    )


class Address(models.Model):
    """Address model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address_name=models.CharField(max_length=100,verbose_name='Address Name',default='')
    region=models.CharField(max_length=200,choices=REGIONS,default='Nairobi')
    phone_number=models.CharField(max_length=20,verbose_name='Phone Number',default='')
    additional_phone_number=models.CharField(
        max_length=20,verbose_name='Additional Phone Number',blank=True,null=True)
    delivery_instructions=models.CharField(
        max_length=100,blank=True,null=True,
        verbose_name='Delivery Instructions |Additional Information')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default_address=models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    def __str__(self):
        return self.address_name

    
   #a method to prevent more than one default address
    def save(self, *args, **kwargs):
        if self.default_address:
            try:
                temp = Address.objects.get(default_address=True)
                if self != temp:
                    temp.default_address = False
                    temp.save()
            except Address.DoesNotExist:
                pass
        super(Address, self).save(*args, **kwargs)




class PickupStation(models.Model):
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    address_name=models.CharField(max_length=100)
    additional_phone_number=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=100)
    region=models.CharField(max_length=200,choices=REGIONS,default='Nairobi')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default_station=models.BooleanField(default=False)


    class Meta: 
        verbose_name = _("Pickup Station")
        verbose_name_plural = _("Pickup Stations")
    
    

    def __str__(self):
        return self.name

    def  get_absolute_url(self):
        return reverse('pickupstation_detail', kwargs={'pk': self.pk})



class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deposited_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    transaction_type = models.CharField(max_length=20)
    description = models.CharField(max_length=100, default='product/service purchased')
    type = models.CharField(default='CUSTOMER', max_length=9)
    payment_done = models.BooleanField(default=False)
    transaction_datetime = models.DateTimeField(auto_now_add=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type}"

    class Meta:
        ordering = ['-transaction_datetime']



class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, related_name='transactions', on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20)
    description = models.CharField(max_length=100, default='product/service purchased')
    type = models.CharField(default='CUSTOMER', max_length=9)
    reference = models.CharField(max_length=6)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    deposited_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    transaction_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.wallet.user.username} - {self.transaction_type}"