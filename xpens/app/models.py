from datetime import date

from django.db import models
from django.conf import settings


class CategoryQuerySet(models.QuerySet):

    def by_name(self, name):
        return self.filter(name=name)

    def by_user(self, user):
        return self.filter(user=user)


class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name="categories")
    description = models.TextField(blank=True,
                                   default="")
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)

    objects = CategoryQuerySet.as_manager()

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ("name", "user",)
        ordering = ['name']


class ExpenseQuerySet(models.QuerySet):

    def between_dates(self, from_date, to_date):
        return self.filter(date__gte=from_date, date__lte=to_date)

    def by_user(self, user):
        return self.filter(user=user)

    def by_user_between_dates(self, user, from_date, to_date):
        return self.by_user(user).between_dates(from_date, to_date)

    def by_user_in_current_month(self, user):
        today = date.today()
        current_month_beginning = date(today.year, today.month, 1)
        return self.by_user(user).between_dates(current_month_beginning,
                                                today)

    def most_recent_expenses_by_user(self, user):
        return self.filter(user=user).order_by("-date", "-created")[:5]

    def distinct_category_names(self):
        return [category['category__name']
                for category in self.values('category__name').distinct()]

    def total_expense_amount_by_category(self, category_name):
        return int(self.filter(category__name=category_name)
                   .aggregate(models.Sum('amount'))['amount__sum'])

    def category_wise_total_for(self, category_names):
        return [self.total_expense_amount_by_category(category_name)
                for category_name in category_names]


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

    objects = ExpenseQuerySet.as_manager()
