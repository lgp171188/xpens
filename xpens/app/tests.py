from datetime import date, timedelta
from random import randint

from django.test import TestCase
from django.contrib.auth.models import User

from .models import (
    Category,
    Expense
)


class ExpenseQuerySetMethodsTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user('guruprasad',
                                              'guruprasad@example.com',
                                              'sample')
        self.user2 = User.objects.create_user('guru',
                                              'guru@example.com',
                                              'sample')
        self.category1 = Category.objects.create(user=self.user1,
                                                 name='Cat1')
        self.category2 = Category.objects.create(user=self.user1,
                                                 name='Cat2')
        self.today = date.today()
        self.tomorrow = self.today + timedelta(days=1)
        self.yesterday = self.today - timedelta(days=1)

    def test_between_dates(self):
        Expense.objects.create(user=self.user1,
                               date=self.today,
                               amount=100.0,
                               description='',
                               category=self.category1
                               )
        hundred_days_back = self.today - timedelta(days=100)
        hundred_days_ahead = self.today + timedelta(days=100)
        expenses1 = Expense.objects.between_dates(self.yesterday,
                                                  self.tomorrow)
        expenses2 = Expense.objects.between_dates(hundred_days_back,
                                                  self.yesterday)
        expenses3 = Expense.objects.between_dates(self.tomorrow,
                                                  hundred_days_ahead)

        self.assertEqual(expenses1.count(), 1)
        self.assertEqual(expenses2.count(), 0)
        self.assertEqual(expenses3.count(), 0)

    def test_between_dates_invalid_date_range(self):
        Expense.objects.create(user=self.user1,
                               date=self.today,
                               amount=100.0,
                               description='',
                               category=self.category1
                               )
        expenses = Expense.objects.between_dates(self.tomorrow,
                                                 self.yesterday)
        self.assertEqual(expenses.count(), 0)

    def test_by_user(self):
        e = Expense.objects.create(user=self.user1,
                                   date=self.today,
                                   amount=100.0,
                                   description='',
                                   category=self.category1
                                   )
        self.assertEqual(Expense.objects.by_user(self.user1).count(), 1)
        self.assertEqual(Expense.objects.by_user(self.user1)[0], e)
        self.assertEqual(Expense.objects.by_user(self.user2).count(), 0)

    def test_by_user_between_dates(self):
        e = Expense.objects.create(user=self.user1,
                                   date=self.today,
                                   amount=123.0,
                                   description='Test expense',
                                   category=self.category1)
        expenses = Expense.objects.by_user_between_dates(self.user1,
                                                         self.yesterday,
                                                         self.tomorrow)
        self.assertEqual(expenses.count(), 1)
        self.assertEqual(expenses[0], e)
        self.assertEqual(Expense.objects.by_user(self.user1)
                         .between_dates(self.yesterday,
                                        self.tomorrow)[0],
                         expenses[0])

    def test_most_recent_expenses_by_user(self):
        for _ in range(3):
            Expense.objects.create(user=self.user1,
                                   date=self.yesterday,
                                   amount=randint(100, 200),
                                   description='',
                                   category=self.category1)
        self.assertEqual(Expense.objects
                         .most_recent_expenses_by_user(self.user1).count(), 3)
        for _ in range(3):
            Expense.objects.create(user=self.user1,
                                   date=self.today,
                                   amount=randint(100, 200),
                                   description='',
                                   category=self.category1)

        self.assertEqual(Expense.objects
                         .most_recent_expenses_by_user(self.user1).count(), 5)
        self.assertEqual(Expense.objects
                         .most_recent_expenses_by_user(self.user2).count(), 0)
