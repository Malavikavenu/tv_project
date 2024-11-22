from django.shortcuts import render,redirect
from django.urls import reverse,reverse_lazy


from store.models import Product,Tag,Cart,CartItems,OrderSummary,Reviews,UserProfile
from django.contrib.auth import authenticate,login,logout

from store.forms import SignUpForm,LoginForm,AddressForm,ReviewForm,UserprofileForm
from django.views.generic import View,TemplateView,DetailView,FormView,UpdateView

from django.contrib import messages

from decouple import config
import razorpay




KEY_SECRET=config('KEY_SECRET')


KEY_ID=config('KEY_ID')
   
    
class SignUpView(View):

    def get(self,request,*args,**kwargs):

        form_instance=SignUpForm()

        return render(request,"store/signup.html",{"form":form_instance})
    
    

    def post(self,request,*args,**kwargs):

        form_instance=SignUpForm(request.POST)

        if form_instance.is_valid():

            form_instance.save()

            return redirect("signin")
        
        else:

            return render(request,"store/signup.html",{"form":form_instance})
        


class SignInView(View):

    def get(self,request,*args,**kwargs):

        form_instance=LoginForm()

        return render(request,"store/login.html",{"form":form_instance})
    

    def post(self,request,*args,**kwargs):

        form_instance=LoginForm(request.POST)

        if form_instance.is_valid():

           data=form_instance.cleaned_data
           user_obj=authenticate(request,**data)


           if user_obj:
               
               login(request,user_obj)

               return redirect("index")
               
        else:
            
            return render(request,"store/login.html",{"form":form_instance})
        
    


    
class IndexView(View):

   template_name="store/index.html"

   def get(self,request,*args,**kwargs):
       
       qs=Product.objects.all()

     

       return render(request,self.template_name,{"products":qs})


class ProductDetailView(DetailView):

    template_name="store/product_detail.html"

    context_object_name="product"

    model=Product 
   


class AddToCartView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")
       
        
       
       
   

        product_obj=Product.objects.get(id=id)
        
      
    

        CartItems.objects.create(cart_object=request.user.basket,
                                 product_object=product_obj,
                                 updated_price=product_obj.price
                                   
                                

                                )
       
       


    

              
        
             
            
                
                                 

                                
        
        # qs=request.user.basket.basket_items.filter(is_order_placed=False)
        
        print("item added to cart")

        return redirect("my-cart")

        # return render(request,"store/index.html",{"item":qs})
    
        

       
    
from django.db.models import Sum
class MyCartView(View):

    def get(self,request,*args,**kwargs):

       
        qs=request.user.basket.basket_items.filter(is_order_placed=False ).order_by("-created_date")
        total_items=qs.count()



   
        


    
       

        
        
        total=request.user.basket.cart_total

        
       

       
  

    



      

        print(total)
        

       

        return render(request,"store/cart_summary.html",{"cartitems":qs,"total":total,"items":total_items})


    
    


class CartItemDeleteView(View):

    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")

        qs=CartItems.objects.get(id=id).delete()

        return redirect("my-cart")
    

class CheckOutView(View):

    def get(self,request,*args,**kwargs):

        form_instance=AddressForm()
        
        if payment_method == 'online_payment':
        client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))                                     #authentication to razorpay

        amount=self.request.user.basket.cart_total*100                                           #total amount in wishlist

        data = { "amount": amount, "currency": "INR", "receipt": "order_rcptid_11" }

        payment = client.order.create(data=data)
  
        form_instance.instance.order_id=payment.get('id')
        form_instance.instance.user_object = request.user
        form_instance.instance.total=request.user.basket.cart_total
        form_instance.save()

        cart_items = self.request.user.basket.basket_items.filter(is_order_placed=False)

        for ci in cart_items:
            form_instance.instance.cart_item_object.add(ci)
            ci.is_order_placed = True
        ci.save()
        form_instance.save()

        context={
                    'key':KEY_ID,
                    'amount':data.get('amount'),
                    'currency':data.get('currency'),
                    'order_id':payment.get('id')
                }



        return render(self.request,'store/payment.html',context,{"form":form_instance})

   
    
    def post(self,request,*args,**kwargs):

        form_instance=AddressForm(request.POST)

        if form_instance.is_valid():

            payment_method = form_instance.cleaned_data['payment_method']
            print('printing....',payment_method)

            if payment_method == 'cash-on-delivery':
                form_instance.instance.user_object = request.user
                form_instance.instance.is_paid=True
                form_instance.instance.total=request.user.basket.total_amount
                form_instance.save()

                cart_items = self.request.user.basket.basket_items.filter(is_order_placed=False)
                

                for ci in cart_items:
                    form_instance.instance.cart_item_object.add(ci)
                    ci.is_order_placed = True
                    ci.save()
                form_instance.save()

                # user_phone = '+919947115118'
                # message = f"Thank you for your payment of Rs. {form_instance.instance.total}. Your order has been placed!"
                # sent_sms(user_phone, message)

                return render(request,"store/cod.html")

            
            el

             

          
    

    
                
           
                
           
            




  

from django.views.decorators.csrf import csrf_exempt

from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt,name="dispatch")
class PaymentVerificationView(View):

    def post(self,request,*args,**kwargs):

        print(request.POST)
        
        client = razorpay.Client(auth=(KEY_ID,KEY_SECRET))
        order_summary_object=OrderSummary.objects.get(order_id=request.POST.get("razorpay_order_id"))
        login(request,order_summary_object.user_object)
        try:
            #doubtfulcode
            client.utility.verify_payment_signature(request.POST)
            print("payment success")
            order_id=request.POST.get("razorpay_order_id")
            OrderSummary.objects.filter(order_id=order_id).update(is_paid=True)
            cart_items=request.user.basket.basket_items.filter(is_order_placed=False)

            for ci in cart_items:
                print("text",ci)
                ci.is_order_placed=True
                ci.save()

        except:

            #handlingcode
             print("payment fail")



       # return render(request,"store/success.html")
        return redirect('index')
    
class MyPurchaseView(View):
    model=OrderSummary

    context_object_name="orders"

    def get(self,request,*args,**kwargs):
        
        
        qs=OrderSummary.objects.filter(user_object=request.user,is_paid=True).order_by('created_date')

        return render(request,"store/order_summary.html",{"orders":qs})
    
    


class ReviewCreateView(FormView):
#url locailhost:8000/project/<int:pk>/review/add/
    template_name="store/review.html"

    form_class=ReviewForm

    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        product_obj=Product.objects.get(id=id)
        

        form_instance=ReviewForm(request.POST)

        
        if form_instance.is_valid:

            form_instance.instance.user_object=request.user

            form_instance.instance.product_objects=product_obj

            form_instance.save()

            return redirect('index')
        else: 
            return render(request,self.template_name,{"form":form_instance})
        

class UserProfileUpdateView(UpdateView):


    model=UserProfile

    form_class=UserprofileForm

    template_name="store/profile_edit.html"

def get_success_url(self):
    return reverse("index")
#or
    # success_url=reverse_lazy("index") 

from django.db.models import Q,QuerySet
class QuantityUpdateView(View):
    def post(self,request,*args,**kwargs):

        cart_id=kwargs.get("pk")

        cart_obj=CartItems.objects.get(id=cart_id)

        update_type=request.POST.get("update")

        cu_quantity=cart_obj.quantity

        cu_price=cart_obj.product_object.price

        # if cart_obj.quantity is None:
        #     cart_obj.quantity=0
        
        if update_type=='increase':

            cart_obj.quantity=cu_quantity+1

          

        elif update_type=='decrease':
            cart_obj.quantity=cu_quantity-1



        cart_obj.updated_price=cu_price*cart_obj.quantity



    
        print(cart_obj.quantity)
        print(cart_obj.updated_price)

        cart_obj.save()

        return redirect('my-cart')


  
   
     



       
       
    




                            
    

   

        






       
