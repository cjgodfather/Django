from django import forms
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import Event

User = get_user_model()


QUANTITY_CHOICES = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
)

ADDRESS_TYPE = [
    ("B", "BILLIING"),
    ("S", "SHIPPING")]
    
CATEGORY = (
    ("M", "MUSIC"),
    ("A", "ART"),
    ("P", "PARTY"),
    ("S", "SPORT"),
    ("B", "BUSINESS"),
)


class TicketForm(forms.Form):
    quantity = forms.ChoiceField(
        choices=QUANTITY_CHOICES, label="", widget=forms.Select()
    )

class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "password", "email", )

class AddressForm(forms.Form):
    street = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'street'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'city'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'state'}))
    country = CountryField().formfield(widget=CountrySelectWidget(attrs={'class':'form-control', 'placeholder':'country'}))
    zip = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'zip'}))
    address_type = forms.ChoiceField(widget=forms.RadioSelect, choices=ADDRESS_TYPE)
    

