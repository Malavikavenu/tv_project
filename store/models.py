from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum,Avg

from django.core.validators import MinValueValidator,MaxValueValidator
import random




class UserProfile(models.Model):

    name=models.CharField(max_length=260,null=True)
    pic=models.ImageField(upload_to="profile_pic",default="/profile_pic/default.png")

    user_object=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    def __str__(self):

        return self.name
    



 
class Tag(models.Model):
    
    title=models.CharField(max_length=100,unique=True)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    def __str__(self):

        return self.title
    
class Product(models.Model):

    brand=models.CharField(max_length=200)
    price=models.PositiveIntegerField()
    image=models.ImageField(upload_to="tv_images")
    description=models.TextField()
    stock=models.IntegerField()
    tag_objects=models.ManyToManyField(Tag)
   
    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)
    
    def __str__(self):

        return self.brand
    

    @property
    def review_count(self):
        return self.product_reviews.all().count()
    
    @property
    def average_rating(self):
        return self.product_reviews.all().values('rating').aggregate(avg=Avg('rating')).get('avg',0)

    
    

class Cart(models.Model):

    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="basket")

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    @property
    def cart_total(self):
        return self.basket_items.filter(is_order_placed=False).values("updated_price").aggregate(total=Sum("updated_price")).get("total")
    


    

   
    
from django.core.exceptions import ValidationError
class CartItems(models.Model):

    cart_object=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="basket_items")

    product_object=models.ForeignKey(Product,on_delete=models.CASCADE)

    quantity=models.PositiveIntegerField(null=True,default=1,validators=[MinValueValidator(1),MaxValueValidator(10)])

    updated_price=models.IntegerField(null=True)

    is_order_placed=models.BooleanField(default=False)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)






     
  
   

       

            
            



class OrderSummary(models.Model):

    user_object=models.ForeignKey(User,on_delete=models.CASCADE,related_name="orders")

    cart_item_object=models.ManyToManyField(CartItems)
    product_object=models.ManyToManyField(Product)

    order_id=models.CharField(max_length=100,null=True)

    is_paid=models.BooleanField(default=False)

    name=models.CharField(max_length=200,null=True)
    phone=models.IntegerField(null=True)
    address=models.TextField(null=True)
    pin=models.IntegerField(null=True)
    payment_options=(
        ("cash_on_delivery","cash_on_delivery"),
        ("online_payment","online_payment"),
        

    )
    payment_method=models.CharField(max_length=200,choices=payment_options,default="online_payment",null=True)



    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)
    total=models.FloatField(null=True)


from django.db.models.signals import post_save

def create_basket(sender,instance,created,*args,**kwargs):

    if created:

        Cart.objects.create(owner=instance)
    
post_save.connect(receiver=create_basket,sender=User)




class Reviews(models.Model):

    product_objects=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_reviews")
    
    user_object=models.ForeignKey(User,on_delete=models.CASCADE)

    comment=models.TextField()

    
    rating=models.PositiveIntegerField(default=1,validators=[MinValueValidator(1),MaxValueValidator(5)])

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)


