# Generated by Django 3.0.8 on 2020-08-10 21:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_auto_20200809_1812'),
    ]

    operations = [
        migrations.RenameField(
            model_name='module',
            old_name='charge_price',
            new_name='price',
        ),
    ]