from django import forms
from django.forms import ModelForm

from .models import *

class NewExpenseForm(ModelForm):
    date = forms.DateField(widget=forms.DateInput(format = '%d/%m/%Y'), 
                           input_formats=('%d/%m/%Y',))
    class Meta:
        model = Expense
        fields = ['date', 'amount', 'description', 'category']

class NewCategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']
