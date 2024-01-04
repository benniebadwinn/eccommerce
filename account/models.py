from django.db import models
from django.contrib.auth.models import User
from PIL import Image


from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model  # current user model
from django.utils.translation import gettext_lazy as _

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
  user = models.CharField(max_length=200)
  email = models.CharField(max_length=200)



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


class WalletTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20)  # 'deposit', 'withdrawal', etc.
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type}"

