# Generated by Django 3.0.8 on 2020-08-08 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moduleregistrationreport',
            name='approved',
        ),
        migrations.RemoveField(
            model_name='moduleregistrationreport',
            name='payed',
        ),
        migrations.AddField(
            model_name='moduleregistrationreport',
            name='status',
            field=models.CharField(choices=[('PEN', 'Pending'), ('DEN', 'Denied'), ('APR', 'Approved'), ('PAY', 'Payed'), ('COM', 'Completed')], default='PEN', max_length=3, verbose_name='Status'),
        ),
    ]
