from django import forms

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

from store.models import Address








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

        model=Address

        fields=["name","phone","address","pin","payment_method"]


        # widget={"name":forms.TextInput(attrs={'class': "form-control mx-auto",
        #                                     'style': 'max-width: 300px;'}),
                                            
        #          "phone":forms.NumberInput(attrs={'class': "form-control p-0",
        #                                         'style': 'max-width: 300px;'}),

        #         "address":forms.Textarea(attrs={"class":"form-control p-0",
        #                                         "style":"max-width:300px"}),


        #         "pin":forms.NumberInput(attrs={'class': "form-control"
        #                                         }),  

        #         "payment_method":forms.Select(attrs={"class":"form-control form-select"}),                        
                                            
                                            
        #                                     }

