from django import forms
from django.forms import ModelForm

from .models import (
    Expense,
    Category,
)


class NewExpenseForm(ModelForm):
    date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),
                           input_formats=('%d/%m/%Y',))

    class Meta:
        model = Expense
        fields = ['date', 'amount', 'description', 'category']
        widgets = {
            'amount': forms.TextInput(),
        }


class NewCategoryForm(ModelForm):

    class Meta:
        model = Category
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(NewCategoryForm, self).__init__(*args, **kwargs)
        self.instance.user = user

    def clean_name(self):
        name = self.cleaned_data['name']
        duplicates = Category.objects.filter(user=self.instance.user, name=name)
        if self.instance.pk:
            duplicates = duplicates.exclude(pk=self.instance.pk)
        if duplicates:
            raise forms.ValidationError("Category already exists")
        return name
