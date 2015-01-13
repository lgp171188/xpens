# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_add_created_modified_fields_expense_category'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set([('name', 'user')]),
        ),
    ]
