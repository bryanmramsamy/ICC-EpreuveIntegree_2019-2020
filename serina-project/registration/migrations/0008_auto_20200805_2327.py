# Generated by Django 3.0.8 on 2020-08-05 21:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0007_auto_20200805_0012'),
    ]

    operations = [
        migrations.RenameField(
            model_name='moduleregistrationreport',
            old_name='student_attempt',
            new_name='nb_attempt',
        ),
    ]