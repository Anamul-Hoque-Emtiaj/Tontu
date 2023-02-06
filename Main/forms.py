from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import ProductReview,UserAddressBook

class SignupForm(UserCreationForm):
	class Meta:
		model=User
		fields=('first_name','last_name','email','username','password1','password2')

		widget = {
			'first_name': forms.TextInput(attrs={'class':'form-control'}),
			'last_name': forms.TextInput(attrs={'class':'form-control'}),
			'email': forms.TextInput(attrs={'class':'form-control'}),
			'username': forms.TextInput(attrs={'class':'form-control'}),
			'password1': forms.TextInput(attrs={'class':'form-control'}),
			'password2': forms.TextInput(attrs={'class':'form-control'})
		}

# Review Add Form
class ReviewAdd(forms.ModelForm):
	class Meta:
		model=ProductReview
		fields=('review_text','review_rating')

# AddressBook Add Form
class AddressBookForm(forms.ModelForm):
	class Meta:
		model=UserAddressBook
		fields=('mobile','street_address','city','country','zipcode')

# ProfileEdit
class ProfileForm(UserChangeForm):
	class Meta:
		model=User
		fields=('first_name','last_name','email','username')