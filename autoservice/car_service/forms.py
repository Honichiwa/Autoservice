from django import forms
from . import models
from .models import Order, Car
from django.contrib.auth import get_user_model


User = get_user_model()

class DateInput(forms.DateInput):
    input_type = 'date'

class OrderCommentForm(forms.ModelForm):
    class Meta:
        model = models.OrderComment
        fields = ('content', 'order', 'commenter')
        widgets = {
            'order': forms.HiddenInput,
            'commenter': forms.HiddenInput,
        }   

class CarForm(forms.ModelForm):
    class Meta:
        model = models.Car
        fields = ('car_nr', 'vin', 'car_model', 'client', 'cover', 'description')
        widgets = {
            'client': forms.HiddenInput(),
        }

class OrderForm(forms.ModelForm):

    class Meta:
        model = models.Order
        fields = ('date', 'car', 'due_back', 'status')
        widgets = {
            'date': DateInput(),
            'car': forms.HiddenInput(),
            'due_back': DateInput(),
            'status': forms.HiddenInput(),
        }

class OrderOForm(forms.ModelForm):

    class Meta:
        model = models.Order
        fields = ('date', 'car', 'due_back', 'status')
        widgets = {
            'date': DateInput(),
            'due_back': DateInput(),
            'status': forms.HiddenInput(),
        }
