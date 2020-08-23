# Generated by Django 3.0.8 on 2020-08-23 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0005_moduleregistrationreport_date_payed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='degreeregistrationreport',
            name='date_end',
        ),
        migrations.RemoveField(
            model_name='degreeregistrationreport',
            name='date_start',
        ),
        migrations.RemoveField(
            model_name='moduleregistrationreport',
            name='date_end',
        ),
        migrations.RemoveField(
            model_name='moduleregistrationreport',
            name='date_start',
        ),
        migrations.AddField(
            model_name='degreeregistrationreport',
            name='date_payed',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Payment date'),
        ),
    ]
