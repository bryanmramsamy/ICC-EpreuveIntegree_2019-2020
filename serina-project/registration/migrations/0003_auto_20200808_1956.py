# Generated by Django 3.0.8 on 2020-08-08 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_auto_20200808_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moduleregistrationreport',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('DENIED', 'Denied'), ('APPROVED', 'Approved'), ('PAYED', 'Payed'), ('COMPLETED', 'Completed')], default='PENDING', max_length=9, verbose_name='Status'),
        ),
    ]
