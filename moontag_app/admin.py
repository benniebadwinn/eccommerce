from django.contrib import admin
from moontag_app.models import Category,Cart,CartProduct,Vendor,OrderItem,Offer,Color,Size,Brand,Product,ProductAttribute,Banner,Coupon,Wishlist,Order, OrderItem,MpesaPayment,CouponUsage, Contact,Feedback,ReviewRating,ShippingCompany,OfferStatus
from moontag_app.models import Category,Color,Size,Brand,Product,ProductAttribute,Todo,Withraw
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _



class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('in_num','product','image_tag','quantity','price','total')
    # raw_id_fields = ['product']
admin.site.register(OrderItem, OrderItemAdmin)


class WithrawAdmin(admin.ModelAdmin):
    list_display = ('user','amount')
admin.site.register(Withraw, WithrawAdmin)

class TodoAdmin(admin.ModelAdmin):
    list_display = ('user','todo')
admin.site.register(Todo, TodoAdmin)



# Register your models here.
@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description', 'image']
    prepopulated_fields = {'slug': ('name',)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title','image_tag')
admin.site.register(Category, CategoryAdmin)





class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','title','category','brand','is_featured','is_data3') # its a tuple but i will remember the name list better
    
admin.site.register(Product, ProductAdmin)


# admin.site.Offer(Offer, OfferAdmin)
@admin.register(Offer)
@admin.register(OfferStatus)




class BrandAdmin(admin.ModelAdmin):
    list_display = ('title',)
admin.site.register(Brand, BrandAdmin)

class ColorAdmin(admin.ModelAdmin):
    list_display = ('title','color_tag')
admin.site.register(Color,ColorAdmin)

class SizeAdmin(admin.ModelAdmin):
    list_display = ('title',)
admin.site.register(Size, SizeAdmin)

class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('id','product','image_tag','price','color','size','stock')
admin.site.register(ProductAttribute, ProductAttributeAdmin)

class BannerAdmin(admin.ModelAdmin):
    list_display = ('text','image_tag')
admin.site.register(Banner, BannerAdmin)




admin.site.register(Contact)
admin.site.register(Feedback)
admin.site.register(ShippingCompany)
admin.site.register(Cart)
admin.site.register(CartProduct)





@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = [
        'code', 'valid_from',
        'valid_to', 'value', 'is_active', 'num_available', 'used']
    list_filter = ['is_active', 'valid_from', 'valid_to']
    search_fields = ['code']



@admin.register(CouponUsage)
class CouponUsageAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'coupon',
        'used_at']
    



# @admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'slug', 'created', 'updated']
    list_filter = ['created', 'updated']
    prepopulated_fields = {'slug': ('product',)}





admin.site.register(Order)
class OrderAdmin(admin.ModelAdmin):                      # The ModelAdmin class is the representation of a model in the admin interface. Usually, these are stored in a file named admin.py in your application. Let’s take a look at an example of the ModelAdmin. ref https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin This class is made so that we can get a separate column in django admin which will show which orders were successful and which were not. Set list_display to control which fields are displayed on the change list page of the admin. If you don’t set list_display, the admin site will display a single column that displays the __str__() representation of each object. ref https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display
    list_display = ['user', 'ordered', 'received', 'billing_address', 'shipping_address', 'payment', 'coupon', 'being_delivered', 'refund_requested', 'refund_granted']                   # user is the heading of one column and "ordered" is the heading of the second column

    list_filter = ['ordered', 'received', 'billing_address', 'shipping_address', 'payment', 'coupon', 'being_delivered', 'refund_requested', 'refund_granted']      # This will create a filter box so that you can filter while searching

    search_fields = ['user__username', 'reference_code']          # we used __username because otherwise an error would come up related to icontains. You can use icontains lookup on text fields. user is related (integer) field. Instead of user use user__username. ref https://stackoverflow.com/questions/35012942/related-field-got-invalid-lookup-icontains            # This is so that we can search based on these fields

    list_display_links = [          # This is to add links in the table of orders in django admin. These entries will have their own rows and will have links
        'user',
        'billing_address',
        'payment',
        'coupon']

    # actions = [make_refund_accepted]        # as par tof the format of making our own actions




admin.site.register(MpesaPayment)


admin.site.register(ReviewRating)  