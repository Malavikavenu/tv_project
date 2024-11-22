"""
URL configuration for Tv_ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from store import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('register/',views.SignUpView.as_view(),name="signup"),

    path("",views.SignInView.as_view(),name="signin"),

    path("index/",views.IndexView.as_view(),name="index"),

    path("product/<int:pk>/",views.ProductDetailView.as_view(),name="product-detail"),

    path('profile/<int:pk>/change/',views.UserProfileUpdateView.as_view(),name="profile-update"),


    path("product/<int:pk>/cart/add/",views.AddToCartView.as_view(),name="add-cart"),

    path("cart/summary/",views.MyCartView.as_view(),name="my-cart"),

    path("cartitem/<int:pk>/remove/",views.CartItemDeleteView.as_view(),name="cartitem-delete"),

    
    path("checkout/",views.CheckOutView.as_view(),name="checkout"),

    path("payment/verify/",views.PaymentVerificationView.as_view(),name="payment-verify"),

    path('order/summary/',views.MyPurchaseView.as_view(),name="order-summary"),

    path('product/<int:pk>/review/add/',views.ReviewCreateView.as_view(),name="review-add"),

    path("cart/item/<int:pk>/update",views.QuantityUpdateView.as_view(),name="cart-update"),
    

    
    
 
    
   
  


    

    

    




   

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


