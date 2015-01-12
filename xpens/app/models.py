from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name="categories")
    description = models.TextField(blank=True,
                                   default="")
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return self.name


class Expense(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=20,
                                 decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(Category,
                                 related_name="expenses",
                                 null=True,
                                 on_delete=models.SET_NULL)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name="expenses")
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)
