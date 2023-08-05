# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Demo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=60, verbose_name='title')),
                ('slug', models.SlugField(unique=True, verbose_name='slug')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
