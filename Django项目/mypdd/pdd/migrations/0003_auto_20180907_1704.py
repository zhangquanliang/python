# Generated by Django 2.0.7 on 2018-09-07 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdd', '0002_auto_20180907_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='pay_url',
            field=models.CharField(max_length=100, verbose_name='付款链接'),
        ),
    ]
