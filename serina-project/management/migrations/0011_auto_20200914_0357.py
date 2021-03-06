# Generated by Django 3.1.1 on 2020-09-14 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0010_auto_20200823_0248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='picture',
            field=models.ImageField(blank=True, default='management/books.png', max_length=225, null=True, upload_to='management/rooms/', verbose_name='Picture'),
        ),
        migrations.AlterField(
            model_name='course',
            name='picture',
            field=models.ImageField(blank=True, default='management/books.png', max_length=225, null=True, upload_to='management/courses/', verbose_name='Picture'),
        ),
        migrations.AlterField(
            model_name='degree',
            name='picture',
            field=models.ImageField(blank=True, default='management/books.png', max_length=225, null=True, upload_to='management/degrees/', verbose_name='Picture'),
        ),
        migrations.AlterField(
            model_name='module',
            name='picture',
            field=models.ImageField(blank=True, default='management/books.png', max_length=225, null=True, upload_to='management/modules/', verbose_name='Picture'),
        ),
    ]
