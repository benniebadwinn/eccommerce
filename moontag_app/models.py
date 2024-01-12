from django.db import models
from django.utils.html import mark_safe # send safely into django data and can put photos to the App in the admin panel
from django.contrib.auth.models import User




import uuid
from django.db import models
from django.utils.html import mark_safe # send safely into django data and can put photos to the App in the admin panel
from django.contrib.auth.models import User
from django.db.models import Sum


from io import BytesIO
from PIL import Image
from django.contrib.auth import get_user_model

from django.core.files import File
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from moontag_app.managers import UserManager

from django.utils.text import slugify
from django.utils.crypto import get_random_string
from account.models import Address,PickupStation
from django.utils.html import mark_safe
from django.db.utils import OperationalError, ProgrammingError





User = get_user_model()


class Customer(models.Model):
    email = models.EmailField(unique=True)
    # Add other customer-related fields as needed

    def __str__(self):
        return self.email

class Newsletter(models.Model):
    subject = models.CharField(max_length=255)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    recipients = models.ManyToManyField(Customer, related_name='newsletters_sent')

    def __str__(self):
        return self.subject


class ChatRoom(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=100)
    img = models.ImageField(upload_to='media/category_images')

    class Meta:
        verbose_name_plural = '1. Categories'

    def image_tag(self):
        return mark_safe('<img src="%s" width="60" height="60" />' % (self.img.url))

    def __str__(self):
        return self.title
    



class Brand(models.Model):
    title = models.CharField(max_length=100)
    img = models.ImageField(upload_to='media/brand_images')

    class Meta:
        verbose_name_plural = '2. Brands'

    def __str__(self):
        return self.title


class Color(models.Model):
    title = models.CharField(max_length=100)
    color_code = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = '3. Colors'

    def color_tag(self):
        return mark_safe('<div style="width:30px; height:30px; background-color:%s"></div>' % (self.color_code))

    def __str__(self):
        return self.title


SIZE_CHOICES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Extra Extra Large'),
    )
class Size(models.Model):
    title = models.CharField(
        max_length=100, blank=True, null=True,choices=SIZE_CHOICES, default='S')

    class Meta:
        verbose_name_plural = '4. Sizes'

    def __str__(self):
        return self.title


# Create your models here.
# class Category(models.Model):
#     title = models.CharField(max_length=100)
#     img = models.ImageField(upload_to='media/category_images')

#     class Meta:
#         verbose_name_plural = '1. Categories'

#     def image_tag(self):
#         return mark_safe('<img src="%s" width="60" height="60" />' % (self.img.url))

#     def __str__(self):
#         return self.title


# class Brand(models.Model):
#     title = models.CharField(max_length=100)
#     img = models.ImageField(upload_to='media/brand_images')

#     class Meta:
#         verbose_name_plural = '2. Brands'

#     def __str__(self):
#         return self.title


# class Color(models.Model):
#     title = models.CharField(max_length=100)
#     color_code = models.CharField(max_length=100)

#     class Meta:
#         verbose_name_plural = '3. Colors'

#     def color_tag(self):
#         return mark_safe('<div style="width:30px; height:30px; background-color:%s"></div>' % (self.color_code))

#     def __str__(self):
#         return self.title


# class Size(models.Model):
#     title = models.CharField(max_length=100)

#     class Meta:
#         verbose_name_plural = '4. Sizes'

#     def __str__(self):
#         return self.title


        
        

        # def get_absolute_url(self):
        #         return reverse('shop:product_detail',
        #                        args=[self.id, self.slug])


        # def __str__(self):                                      # in every model you should define the standard Python class method __str__() to return a human-readable string for each object. This string is used to represent individual records in the administration site (and anywhere else you need to refer to a model instance). Often this will return a title or name field from the model. (ref: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Models)  
        #         return self.title
    
        # def get_absolute_url(self):                             # Define a get_absolute_url() method to tell Django how to calculate the canonical (absolute, recognized) URL for an object. The reverse() function is usually the best approach to be used with get_absolute. One place Django uses get_absolute_url() is in the admin app.  If it makes sense for your model’s instances to each have a unique URL, you should define get_absolute_url(). It’s good practice to use get_absolute_url() in templates, instead of hard-coding your objects’ URLs.  The logic here is that if you change the URL structure of your objects, even for something small like correcting a spelling error, you don’t want to have to track down every place that the URL might be created. Specify it once, in get_absolute_url() and have all your other code call that one place.
        #         # return reverse('shop:product-page', kwargs={self.id, self.slug})     # "SLUG" from line 26 models.py. "self.slug" is as per the format. "core" from urls.py from line 11 and product-page from line 18. The reverse() function can reverse a large variety of regular expression patterns for URLs, but not every possible one.  kwargs allows you to handle named arguments that you have not defined in advance. ref to for format: https://docs.djangoproject.com/en/3.2/ref/models/instances/#get-absolute-url
        #         return reverse('shop:product_page', kwargs={'id': self.id, 'slug': self.slug})


        # # def image_tag(self):
        # #     return mark_safe('<img src="%s" width="60" height="60" />' % (self.img.url))

        # def get_addition_to_cart_url(self):                     # This function was created mainly because to help with the add to cart feature
        #         return reverse('shop:add-to-cart', kwargs={'slug': self.slug})     # "SLUG" from line 26 models.py. "self.slug" is as per the format. "core" from urls.py from line 11 and add-to-cart is from line 20. The reverse() function can reverse a large variety of regular expression patterns for URLs, but not every possible one.  kwargs allows you to handle named arguments that you have not defined in advance. ref to for format: https://docs.djangoproject.com/en/3.2/ref/models/instances/#get-absolute-url
    
        # def get_remove_item_from_cart(self):                     # This function was created mainly because to help with the add to cart feature
        #         return reverse('shop:remove-from-cart', kwargs={'slug': self.slug})     # "SLUG" from line 26 models.py. "self.slug" is as per the format. "core" from urls.py from line 11 and add-to-cart is from line 20. The reverse() function can reverse a large variety of regular expression patterns for URLs, but not every possible one.  kwargs allows you to handle named arguments that you have not defined in advance. ref to for format: https://docs.djangoproject.com/en/3.2/ref/models/instances/#get-absolute-url

    
            
        
    #     class Meta:
    #         verbose_name_plural = '5. Products'
    #         ordering = ['name']
    #         indexes = [
    #             models.Index(fields=['id', 'slug']),
    #             models.Index(fields=['name']),
    #             models.Index(fields=['-created']),
    #         ]
        

 
    # except (OperationalError, ProgrammingError):
    #         pass

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    owner=models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
        related_name='vendor', null=True, blank=True)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=True)
    phone_number=models.CharField(max_length=15, blank=True, null=True)
    email=models.EmailField(blank=True, null=True)
    location=models.CharField(max_length=100,default='Nairobi')
    image = models.ImageField(upload_to='vendors/', blank=True)
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'vendor'
        verbose_name_plural = 'vendors'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:vendor_details', args=[self.slug])





class Vendors(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    store_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    store_img = models.ImageField(upload_to="media/store_images",null=True)
    business_email = models.EmailField(max_length=254)
    pay_pal = models.EmailField(max_length=254)

    class Meta:
        verbose_name_plural = 'A12. Vendors'

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="60" height="60" />' % (self.img))



class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    detail = models.TextField()
    specs = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    in_the_box=models.CharField(max_length=100, blank=True, null=True)
    key_features = models.TextField(blank=True)
    sku = models.CharField(max_length=50, blank=True, null=True)
    model=models.CharField(max_length=100, blank=True, null=True)
    size_of_package = models.CharField(
        max_length=100, blank=True, null=True, choices=SIZE_CHOICES, default='S')
    weight = models.DecimalField(
        max_digits=10, decimal_places=2,verbose_name='Weight (kg)',blank=True, null=True)
    main_material = models.CharField(max_length=100, blank=True, null=True)
    care_instructions = models.TextField(blank=True,verbose_name='Care Label',null=True)
    num_visits = models.IntegerField(default=0)
    last_visit = models.DateTimeField(blank=True, null=True)
    view_count = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    users_wishlist = models.ManyToManyField(User, related_name='wishlist', blank=True)
    vendor=models.ForeignKey(Vendor,related_name='products',on_delete=models.CASCADE,blank=True,null=True)
    status = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    top_rated = models.BooleanField(default=False)
    is_data2 = models.BooleanField(default=False)
    is_data3 = models.BooleanField(default=False)
    
    


    class Meta:
        verbose_name_plural = '5. Products'

    def __str__(self):
        return self.title
    


class VendorAddProduct(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'A13. Vendors Products'


# class Banner(models.Model):
#     img = models.ImageField(upload_to='media/banner_images')
#     text = models.CharField(max_length=300)

#     def image_tag(self):
#         return mark_safe('<img src="%s" width="90"/>' % (self.img.url))

#     def __str__(self):
#         return self.text

#     class Meta:
#         verbose_name_plural = '6. Banners'

# class ProductAttribute(models.Model):
#     product = models.ForeignKey(Product,on_delete=models.CASCADE)
#     color = models.ForeignKey(Color,on_delete=models.CASCADE)
#     size = models.ForeignKey(Size,on_delete=models.CASCADE)
#     price = models.PositiveBigIntegerField()
#     img = models.ImageField(upload_to="media/product_images",null=True)
    
#     class Meta:
#         verbose_name_plural = '7. Product Attribute'

#     def __str__ (self):
#         return self.product.title 

#     def image_tag(self):
#         return mark_safe('<img src="%s" width="60" height="60" />' % (self.img.url))


# class CartOrder(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     total_amt = models.FloatField()
#     paid_status = models.BooleanField(default=False)
#     order_dt = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         verbose_name_plural = '8. Cart order'

# class CartOrderItems(models.Model):
#     order = models.ForeignKey(CartOrder,on_delete=models.CASCADE)
#     in_num = models.CharField(max_length=150)
#     item = models.CharField(max_length=150)
#     img = models.CharField(max_length=200)
#     qty = models.IntegerField()
#     price = models.FloatField()
#     total = models.FloatField() # save according the price and qty

#     class Meta:
#         verbose_name_plural = '9. Cart order items'

#     def image_tag(self):
#         return mark_safe('<img src="/media/%s" width="60" height="60" />' % (self.img))


# RATING = (
#     (1,'1'),
#     (2,'2'),
#     (3,'3'),
#     (4,'4'),
#     (5,'5'),
# )

# class ProductReview(models.Model):
#     user = models.CharField(max_length=100,editable=False)
#     product = models.CharField(max_length=100,editable=False)
#     review_text = models.TextField()
#     review_rating = models.CharField(choices=RATING, max_length=150)
    
#     class Meta:
#         verbose_name_plural = 'A10. Product Review'


# class Wishlist(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     product = models.ForeignKey(Product,on_delete=models.CASCADE)

#     class Meta:
#         verbose_name_plural = 'A11. Wishlist'

# class Vendors(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     store_name = models.CharField(max_length=100)
#     company_name = models.CharField(max_length=100)
#     store_img = models.ImageField(upload_to="media/store_images",null=True)
#     business_email = models.EmailField(max_length=254)
#     pay_pal = models.EmailField(max_length=254)

#     class Meta:
#         verbose_name_plural = 'A12. Vendors'

#     def image_tag(self):
#         return mark_safe('<img src="/media/%s" width="60" height="60" />' % (self.img))


# class VendorAddProduct(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     product = models.ForeignKey(Product,on_delete=models.CASCADE)

#     class Meta:
#         verbose_name_plural = 'A13. Vendors Products'


class Todo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    todo = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'A14. Todo'


class Withraw(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField()

    class Meta:
        verbose_name_plural = 'A15. Withraw'




    
class Offer(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    end_time = models.DateTimeField()
    recipient_email = models.EmailField()



class OfferStatus(models.Model):
    title = models.CharField(max_length=100)
    created = models.BooleanField(default=False)



# class Product(models.Model):
#     try:
#         title = models.CharField(max_length=200)
#         slug = models.SlugField(max_length=200)
#         # image = models.ImageField(upload_to='products/%Y/%m/%d',null=True,blank=True)
#         description = models.TextField(blank=True)
#         #specifications
#         in_the_box=models.CharField(max_length=100, blank=True, null=True)
#         key_features = models.TextField(blank=True)
#         sku = models.CharField(max_length=50, blank=True, null=True)
#         model=models.CharField(max_length=100, blank=True, null=True)
#         size_of_package = models.CharField(
#             max_length=100, blank=True, null=True, choices=SIZE_CHOICES, default='S')
#         weight = models.DecimalField(
#             max_digits=10, decimal_places=2,verbose_name='Weight (kg)',blank=True, null=True)
#         main_material = models.CharField(max_length=100, blank=True, null=True)
#         care_instructions = models.TextField(blank=True,verbose_name='Care Label',null=True)
#         available = models.BooleanField(default=True)
#         is_featured = models.BooleanField(default=False)
#         top_rated = models.BooleanField(default=False)
        
#         num_visits = models.IntegerField(default=0)
#         last_visit = models.DateTimeField(blank=True, null=True)
#         category = models.ForeignKey(Category,on_delete=models.CASCADE)
    
#         brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
      
#         created = models.DateTimeField(auto_now_add=True)
#         updated = models.DateTimeField(auto_now=True)
#         view_count = models.PositiveIntegerField(default=0)
#         vendor=models.ForeignKey(
#             Vendor,related_name='products',on_delete=models.CASCADE,blank=True,null=True)
#         # users_wishlist = models.ManyToManyField(User, related_name="user_wishlist", blank=True)
        
        

#         def get_absolute_url(self):
#                 return reverse('shop:product_detail',
#                                args=[self.id, self.slug])


#         def __str__(self):                                      # in every model you should define the standard Python class method __str__() to return a human-readable string for each object. This string is used to represent individual records in the administration site (and anywhere else you need to refer to a model instance). Often this will return a title or name field from the model. (ref: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Models)  
#                 return self.title
    
#         def get_absolute_url(self):                             # Define a get_absolute_url() method to tell Django how to calculate the canonical (absolute, recognized) URL for an object. The reverse() function is usually the best approach to be used with get_absolute. One place Django uses get_absolute_url() is in the admin app.  If it makes sense for your model’s instances to each have a unique URL, you should define get_absolute_url(). It’s good practice to use get_absolute_url() in templates, instead of hard-coding your objects’ URLs.  The logic here is that if you change the URL structure of your objects, even for something small like correcting a spelling error, you don’t want to have to track down every place that the URL might be created. Specify it once, in get_absolute_url() and have all your other code call that one place.
#                 # return reverse('shop:product-page', kwargs={self.id, self.slug})     # "SLUG" from line 26 models.py. "self.slug" is as per the format. "core" from urls.py from line 11 and product-page from line 18. The reverse() function can reverse a large variety of regular expression patterns for URLs, but not every possible one.  kwargs allows you to handle named arguments that you have not defined in advance. ref to for format: https://docs.djangoproject.com/en/3.2/ref/models/instances/#get-absolute-url
#                 return reverse('shop:product_page', kwargs={'id': self.id, 'slug': self.slug})


#         # def image_tag(self):
#         #     return mark_safe('<img src="%s" width="60" height="60" />' % (self.img.url))

#         def get_addition_to_cart_url(self):                     # This function was created mainly because to help with the add to cart feature
#                 return reverse('shop:add-to-cart', kwargs={'slug': self.slug})     # "SLUG" from line 26 models.py. "self.slug" is as per the format. "core" from urls.py from line 11 and add-to-cart is from line 20. The reverse() function can reverse a large variety of regular expression patterns for URLs, but not every possible one.  kwargs allows you to handle named arguments that you have not defined in advance. ref to for format: https://docs.djangoproject.com/en/3.2/ref/models/instances/#get-absolute-url
    
#         def get_remove_item_from_cart(self):                     # This function was created mainly because to help with the add to cart feature
#                 return reverse('shop:remove-from-cart', kwargs={'slug': self.slug})     # "SLUG" from line 26 models.py. "self.slug" is as per the format. "core" from urls.py from line 11 and add-to-cart is from line 20. The reverse() function can reverse a large variety of regular expression patterns for URLs, but not every possible one.  kwargs allows you to handle named arguments that you have not defined in advance. ref to for format: https://docs.djangoproject.com/en/3.2/ref/models/instances/#get-absolute-url

    
            
        
#         class Meta:
#             verbose_name_plural = '5. Products'
#             ordering = ['name']
#             indexes = [
#                 models.Index(fields=['id', 'slug']),
#                 models.Index(fields=['name']),
#                 models.Index(fields=['-created']),
#             ]
        

 
#     except (OperationalError, ProgrammingError):
#             pass
    

class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, unique=True)
    img = models.ImageField(upload_to="media/product_images/%Y/%m/%d",null=True,blank=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.PositiveBigIntegerField()
    # discountprice = models.PositiveBigIntegerField(null=True, blank=True)
    discountprice = models.PositiveBigIntegerField(null=True, blank=True)
    size_of_package = models.CharField(
        max_length=100, blank=True, null=True, choices=SIZE_CHOICES, default='S')
    stock = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    users_wishlist = models.ManyToManyField(User, related_name='wishlist', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    offer = models.ForeignKey(Offer, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    users_wishlist = models.ManyToManyField(User, related_name="user_wishlist", blank=True)

    def __str__ (self):
        return self.product.title

    def image_tag(self):
        return mark_safe('<img src="%s" width="60" height="60" />' % (self.img.url))
    

    def get_absolute_url(self):
            return reverse('shop:product_detail',
                           args=[self.id, self.slug])

    def get_absolute_url(self):                             # Define a get_absolute_url() method to tell Django how to calculate the canonical (absolute, recognized) URL for an object. The reverse() function is usually the best approach to be used with get_absolute. One place Django uses get_absolute_url() is in the admin app.  If it makes sense for your model’s instances to each have a unique URL, you should define get_absolute_url(). It’s good practice to use get_absolute_url() in templates, instead of hard-coding your objects’ URLs.  The logic here is that if you change the URL structure of your objects, even for something small like correcting a spelling error, you don’t want to have to track down every place that the URL might be created. Specify it once, in get_absolute_url() and have all your other code call that one place.
            return reverse('shop:product-page', kwargs={'slug': self.slug})     # "SLUG" from line 26 models.py. "self.slug" is as per the format. "core" from urls.py from line 11 and product-page from line 18. The reverse() function can reverse a large variety of regular expression patterns for URLs, but not every possible one.  kwargs allows you to handle named arguments that you have not defined in advance. ref to for format: https://docs.djangoproject.com/en/3.2/ref/models/instances/#get-absolute-url

    def get_addition_to_cart_url(self):                     # This function was created mainly because to help with the add to cart feature
            return reverse('shop:add-to-cart', kwargs={'slug': self.slug})     # "SLUG" from line 26 models.py. "self.slug" is as per the format. "core" from urls.py from line 11 and add-to-cart is from line 20. The reverse() function can reverse a large variety of regular expression patterns for URLs, but not every possible one.  kwargs allows you to handle named arguments that you have not defined in advance. ref to for format: https://docs.djangoproject.com/en/3.2/ref/models/instances/#get-absolute-url

    def get_remove_item_from_cart(self):                     # This function was created mainly because to help with the add to cart feature
            return reverse('shop:remove-from-cart', kwargs={'slug': self.slug})     # "SLUG" from line 26 models.py. "self.slug" is as per the format. "core" from urls.py from line 11 and add-to-cart is from line 20. The reverse() function can reverse a large variety of regular expression patterns for URLs, but not every possible one.  kwargs allows you to handle named arguments that you have not defined in advance. ref to for format: https://docs.djangoproject.com/en/3.2/ref/models/instances/#get-absolute-url

        
    
    class Meta:
        verbose_name_plural = '5. Productattribute'
        ordering = ['product']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['product']),
            models.Index(fields=['-created']),
        ]
          










class Banner(models.Model):
    img = models.ImageField(upload_to='media/banner_images')
    text = models.CharField(max_length=300)

    def image_tag(self):
        return mark_safe('<img src="%s" width="90"/>' % (self.img.url))

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = '6. Banners'







class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m/%d')
    thumb_nail=models.ImageField(
        upload_to='products/%Y/%m/%d',null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)
    


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject



class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    value = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    num_available = models.IntegerField(default=1)
    used = models.IntegerField(default=0)
    min_purchase_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    for_new_users = models.BooleanField(default=False)
    users = models.ManyToManyField(User, related_name='coupons', blank=True)

    def __str__(self):
        return self.code
    

   


class CouponUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    value = models.FloatField(default=0.0)

    used_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} used {self.coupon.code} on {self.used_at}"





class Wishlist(models.Model):
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlists')
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlists')
    slug=models.SlugField(max_length=200,blank=True,null=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['-created']

    def __str__(self):
        return f'{self.product.name} in {self.user.email} wishlist'

    def get_absolute_url(self):
        return reverse('moontag_app:product_detail',
                       args=[self.product.id, self.product.slug])
    



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

    

class ShippingCompany(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=True)
    phone_number=models.CharField(max_length=15, blank=True, null=True)
    email=models.EmailField(blank=True, null=True)
    location=models.CharField(max_length=100,default='Nairobi')
    image = models.ImageField(upload_to='shipping_companies/', blank=True)
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'shipping company'
        verbose_name_plural = 'shipping companies'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('orders:shipping_company_details', args=[self.slug])
    



class Order(models.Model):
    ORDER_STATUS = (
        ('pending', _('Pending')),
        ('waiting_fulfillment', _('Waiting Fulfillment')),
        ('processing', _('Processing')),
        ('shipped', _('Shipped')),
        ('out_for_delivery', _('Out for Delivery')),
        ('delivered', _('Delivered')),
        ('cancelled', _('Cancelled')),
    )

    PAYMENT_METHOD = (
        ('mpesa_on_delivery', _('Mpesa on Delivery')),
        ('mpesa', _('Mpesa')),
        ('pesapal', _('Pesapal')),
        ('paypal', _('Paypal')),
    )
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, null=True, blank=True)
    pickup_station = models.ForeignKey(
        PickupStation, on_delete=models.CASCADE, null=True, blank=True)
    order_number = models.CharField(max_length=9, blank=True, null=True, unique=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    
   
    order_status = models.CharField(
        max_length=50, choices=ORDER_STATUS, default='pending')
    created = models.DateTimeField(auto_now_add=True)
    # ordered_date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    ordered = models.BooleanField(default=False)
    payment_method = models.CharField(
        max_length=50, choices=PAYMENT_METHOD, default='mpesa_on_delivery')
    returnable = models.BooleanField(default=True)
    delivered_by = models.ForeignKey(
        ShippingCompany, related_name='orders', null=True, blank=True, on_delete=models.SET_NULL)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.10)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    
    def __str__(self):
        user_str = f' User: {self.user.username}' if self.user and self.user.username else ''
        print(f"DEBUG: Order ID: {self.id}" + user_str)
        return f'Order ID: {self.id}' + user_str

      
    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]



    def get_absolute_url(self):
        return reverse('orders:order_detail', kwargs={'order_number': self.order_number})


    #method to apply coupon
    def apply_coupon(self,coupon):
        self.coupon=coupon
        self.save()



    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = get_random_string(
                length=9, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

        # Calculate and set the tax amount before saving
        

        super().save(*args, **kwargs)



    def shipping_cost(self):
        shipping_cost=0
        for item in self.items.all():
            if item.product.size_of_package=='small':
                shipping_cost+=20
            elif item.product.size_of_package=='medium':
                shipping_cost+=50
            elif item.product.size_of_package=='large':
                shipping_cost+=70
            elif item.product.size_of_package=='extra large':
                shipping_cost+=100
            elif item.product.size_of_package=='extra extra large':
                shipping_cost+=150
        if self.address:
            if self.address.region=='Nairobi':
                shipping_cost+=100
            elif self.address.region=='Mombasa':
                shipping_cost+=200
            elif self.address.region=='Kisumu':
                shipping_cost+=300
            elif self.address.region=='Nakuru':
                shipping_cost+=400
            elif self.address.region=='Eldoret':
                shipping_cost+=500
            elif self.address.region=='Nyeri':
                shipping_cost+=600
            elif self.address.region=='Kakamega':
                shipping_cost+=700
            elif self.address.region=='Kisii':
                shipping_cost+=800
            elif self.address.region=='Meru':
                shipping_cost+=900
            elif self.address.region=='Nanyuki':
                shipping_cost+=1000
            elif self.address.region=='Kericho':
                shipping_cost+=1100
            elif self.address.region=='Kerugoya':
                shipping_cost+=1200
            elif self.address.region=='Kilifi':
                shipping_cost+=1300
            elif self.address.region=='Kisumu':
                shipping_cost+=1400
            elif self.address.region=='Kitale':
                shipping_cost+=1500
            elif self.address.region=='Kisumu':
                shipping_cost+=1600
            elif self.address.region=='Kisumu':
                shipping_cost+=1700
            elif self.address.region=='Kisumu':
                shipping_cost+=1800
            elif self.address.region=='Kisumu':
                shipping_cost+=1900
        return shipping_cost
    

    def check_returnable(self):
        if self.order_status=='delivered':
            if self.updated.date() + timedelta(days=15) < date.today():
                self.returnable=False
                self.save()
        return self.returnable

    #a method to show the returnable deadline date
    def get_returnable_deadline(self):
        if self.order_status=='delivered':
            return self.updated.date() + timedelta(days=15)
        return None

    #a method to check  deliverly method.if via pickup station or address
    #IF pickup station return via pickup station,if address return via Door Delivery
    def delivery_method(self):
        if self.pickup_station:
            return 'Pickup Station'
        elif self.pickup_station is None:
            return 'Door Delivery'
        return  'Door Delivery'


    #method to check shipping company,if None return Esoko Express Delivery
    def shipping_company(self):
        if self.delivered_by:
            return self.delivered_by.name
        return 'Badwin Express Delivery'
    


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    in_num = models.CharField(max_length=150)
    # product = models.ForeignKey(ProductAttribute,
    #                             related_name='order_items',
    #                             on_delete=models.CASCADE)
    product = models.CharField(max_length=150)
    img = models.ImageField(upload_to="media/product_images/%Y/%m/%d",null=True,blank=True)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    quantity = models.DecimalField(max_digits=10,
                                decimal_places=2)
    total = models.DecimalField(max_digits=10,
                                decimal_places=2)
 
    def __str__(self):
        return "Order: " + str(self.order.id) + " OrderItem: " + str(self.id)
    
    def image_tag(self):
        return mark_safe('<img src="%s" width="60" height="60" />' % (self.img.url))

    def get_cost(self):
        return self.price * self.quantity





class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category="color",is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category="size",is_active=True)



variation_category_choice=(
    ('color', 'color'),
    ('size', 'size'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart: " + str(self.id)
    


    def total_items(self):
        """
        Calculate and return the total quantity of items in the cart.
        """
        return sum(item.quantity for item in self.cartproduct_set.all())


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart,related_name='cartproduct_set', on_delete=models.CASCADE)
    product = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return "Cart: " + str(self.cart.id) + " CartProduct: " + str(self.id)
    
    def get_amount_saved(self):
        # Calculate the saved amount if there is a discount
        if self.product.discount_price:
            original_total = self.quantity * self.product.price
            discounted_total = self.quantity * self.product.discount_price
            return original_total - discounted_total
        else:
            return 0
    # def get_cost(self):
    #     return self.price * self.quantity

class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# M-pesa Payment models

class MpesaCalls(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()

    class Meta:
        verbose_name = 'Mpesa Call'
        verbose_name_plural = 'Mpesa Calls'


class MpesaCallBacks(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()

    class Meta:
        verbose_name = 'Mpesa Call Back'
        verbose_name_plural = 'Mpesa Call Backs'


class MpesaPayment(BaseModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    type = models.TextField()
    reference = models.TextField()
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.TextField()
    organization_balance = models.DecimalField(max_digits=10, decimal_places=2)
    is_finished = models.BooleanField(default=False)
    is_successful = models.BooleanField(default=False)
    trans_id = models.CharField(max_length=30, blank=True, null=True)
    order_id = models.CharField(max_length=200, blank=True, null=True)
    checkout_request_id = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Mpesa Payment'
        verbose_name_plural = 'Mpesa Payments'
        indexes = [
            models.Index(fields=['created_at']),
        ]

        
    def __str__(self):
        return self.first_name







class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_address = models.EmailField(max_length=150)
    message = models.CharField(max_length=2000)

    def __str__(self):
        return self.first_name
    
    class Meta:
        verbose_name='Contact'
        verbose_name_plural = 'Contacts'




class Feedback(models.Model):
    name=models.CharField(max_length=40)
    feedback=models.CharField(max_length=500)
    email=models.EmailField(max_length=100)
    date= models.DateField(auto_now_add=True,null=True)

    class Meta:
        verbose_name='Feedback'
        verbose_name_plural = 'Feedbacks'

    def __str__(self):
        return self.name

