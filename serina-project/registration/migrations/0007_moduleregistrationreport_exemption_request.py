# Generated by Django 3.1.1 on 2020-09-22 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0006_auto_20200823_0312'),
    ]

    operations = [
        migrations.AddField(
            model_name='moduleregistrationreport',
            name='exemption_request',
            field=models.BooleanField(default=False, verbose_name='Student exemption request'),
        ),
    ]