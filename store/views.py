from django.shortcuts import render,redirect

from store.models import Product,Tag,Cart,CartItems,OrderSummary,Address
from django.contrib.auth import authenticate,login

from store.forms import SignUpForm,LoginForm,AddressForm
from django.views.generic import View,TemplateView,DetailView

from django.contrib import messages

from decouple import config




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
                                 product_object=product_obj)
        
        print("item added to cart")

        return redirect("index")
    
from django.db.models import Sum
class MyCartView(View):

    def get(self,request,*args,**kwargs):

        qs=request.user.basket.basket_items.filter(is_order_placed=False)

        total=request.user.basket.cart_total

        print(total)

        return render(request,"store/cart_summary.html",{"cartitems":qs,"total":total})
    


class CartItemDeleteView(View):

    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")

        qs=CartItems.objects.get(id=id).delete()

        return redirect("my-cart")
    

class AddressAddView(View):

    def get(self,request,*args,**kwargs):

        form_instance=AddressForm()



        return render(request,"store/address.html",{"form":form_instance})
    

    def post(self,request,*args,**kwargs):

        form_instance=AddressForm(request.POST)

        if form_instance.is_valid():

            order=form_instance.save()

            payment_method=form_instance.cleaned_data['payment_method']

            if payment_method=='online_payment':

                return redirect("checkout")
                
           
            else:

                return render(request,"store/cod.html",{"form":form_instance})
            



import razorpay
class CheckOutView(View):

    def get(self,request,*args,**kwargs):

         
        client = razorpay.Client(auth=(KEY_ID,KEY_SECRET))

        amount = request.user.basket.cart_total*100

        data = { "amount": amount, "currency": "INR", "receipt": "order_rcptid_11" }

       
        payment = client.order.create(data=data)

        purchase_items=request.user.basket.basket_items.filter(is_order_placed=False)

        order_summary_object=OrderSummary.objects.create(user_object=request.user,
                                                         order_id=payment.get("id"),
                                                         
                                                         )
        # order_summary_object.product_objects.add(purchase_items.values("product_object"))

        # for p in purchase_items.values("product_object"):
        #     order_summary_object.product_objects.add(p.get("id"))

        # for pi in purchase_items:
        #     pi.is_order_placed=True
        #     pi.save()


        for pi in purchase_items:

           order_summary_object.product_objects.add(pi.product_object)

           order_summary_object.save()


      
 
        print(payment)

        context={
            "key":KEY_ID,
            "amount":data.get("amount"),
            "currency":data.get("currency"),
            "order_id":payment.get("id"),


        }

        return render(request,"store/payment.html")
    

from django.views.decorators.csrf import csrf_exempt

from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt,name="dispatch")
class PaymentVerificationView(View):

    def post(self,request,*args,**kwargs):

        print(request.POST)

        return render(request,"store/success.html")








