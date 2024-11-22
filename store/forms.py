from django import forms

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

from store.models import Reviews,UserProfile,OrderSummary





class UserprofileForm(forms.ModelForm):

    class Meta:

        model=UserProfile

        fields=["name","pic"]

        widgets={
                    "name":forms.TextInput(attrs={"class":"w-full border p-2 my-3"}),
                    "pic":forms.FileInput(attrs={"class":"w-full border p-2 my-3"})
        }





class SignUpForm(UserCreationForm):

    password1=forms.CharField(widget=forms.PasswordInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'password'
                }))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'confirm password'
                }))


    class Meta:

        model=User

        fields=["username","email","password1","password2"]

        widgets={
                    "username":forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Name'
                }),
                    "email":forms.EmailInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Email'
                })
        }


class LoginForm(forms.Form):

    username=forms.CharField(widget=forms.TextInput(attrs={'style': 'max-width: 300px;','placeholder':'Name','class':"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'style': 'max-width: 300px;','placeholder':'Password','class':"form-control"}))




class AddressForm(forms.ModelForm):

    
    class Meta:

        model=OrderSummary

        fields=["name","phone","address","pin","payment_method"]

        widgets={
                    "name":forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;'
                
                }),
                      "phone":forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;'
                
                }),
                      "address":forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;'
                
                }),
                      "pin":forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;'
                
                }),
                      "payment_method":forms.Select(attrs={
                'class': "form-control form-select",
                'style': 'max-width: 300px;'
                
                }),
        }



class ReviewForm(forms.ModelForm):
    class Meta:
        model=Reviews
        fields=['comment','rating']

        widgets={ "comment":forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;'
                
                }),
                 "rating":forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;'
                
                })

        }
        