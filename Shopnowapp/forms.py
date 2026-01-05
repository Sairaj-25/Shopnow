from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'address', 'city', 'state', 'pin_code', 'landmark']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name', 'required': True}),
            'phone': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number', 'required': True}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter address', 'required': True}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter city', 'required': True}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter state', 'required': True}),
            'pin_code': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter pin code', 'required': True}),
            'landmark': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter landmark (optional)'}),
        }
