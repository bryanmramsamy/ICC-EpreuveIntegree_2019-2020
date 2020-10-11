# Generated by Django 3.1.1 on 2020-10-10 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0014_auto_20201010_0407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='degree',
            name='modules',
            field=models.ManyToManyField(blank=True, help_text='All the modules which are part of the degree.', related_name='degrees', to='management.Module', verbose_name='Modules'),
        ),
    ]