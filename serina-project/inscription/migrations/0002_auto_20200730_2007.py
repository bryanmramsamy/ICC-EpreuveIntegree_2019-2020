# Generated by Django 3.0.8 on 2020-07-30 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inscription', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentregistrationreport',
            name='additional_address',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Additional address'),
        ),
    ]
