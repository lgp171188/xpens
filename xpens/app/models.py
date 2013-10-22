from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, related_name="categories")

    def __unicode__(self):
        return self.name

class Expense(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(Category, related_name="expenses", null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, related_name="expenses")
