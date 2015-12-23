# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cloud',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cloudname', models.CharField(max_length=50)),
                ('endpoint', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CloudUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('clouduser', models.CharField(max_length=50)),
                ('cloudpassword', models.CharField(max_length=50)),
                ('project', models.CharField(default=b'demo', max_length=20)),
                ('cloud', models.ForeignKey(related_name='cloud', to='hybrid_cloud.Cloud')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='clouduser',
            name='user',
            field=models.ForeignKey(related_name='user', to='hybrid_cloud.User'),
            preserve_default=True,
        ),
    ]
