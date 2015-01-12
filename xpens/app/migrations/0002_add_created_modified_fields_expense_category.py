# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

import pytz

from django.db import models, migrations
from django.conf import settings

def update_created_modified_timestamps_expense(apps, schema_editor):
    Expense = apps.get_model("app", "Expense")
    for expense in Expense.objects.filter(created=None):
        created = datetime.combine(expense.date,
                                   datetime.min.time())
        current_tz = pytz.timezone(settings.TIME_ZONE)
        expense.created = current_tz.localize(created)
        expense.modified = expense.created
        expense.save()

def reverse_created_modified_timestamps_expense(apps, schema_editor):
    Expense = apps.get_model("app", "Expense")
    for expense in Expense.objects.all():
        expense.created = None
        expense.modified = None
        expense.save()

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='modified',
            field=models.DateTimeField(auto_now=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='expense',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='expense',
            name='modified',
            field=models.DateTimeField(auto_now=True, null=True),
            preserve_default=True,
        ),
        migrations.RunPython(update_created_modified_timestamps_expense,
                             reverse_created_modified_timestamps_expense),
    ]
