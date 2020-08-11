# Generated by Django 3.0.8 on 2020-08-11 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_auto_20200810_2346'),
    ]

    operations = [
        migrations.AddField(
            model_name='classroom',
            name='picture',
            field=models.ImageField(blank=True, default='management/resource_img/default.jpg', height_field=500, max_length=225, null=True, upload_to='management/resource_img/', verbose_name='Picture', width_field=1000),
        ),
        migrations.AddField(
            model_name='course',
            name='picture',
            field=models.ImageField(blank=True, default='management/resource_img/default.jpg', height_field=500, max_length=225, null=True, upload_to='management/resource_img/', verbose_name='Picture', width_field=1000),
        ),
        migrations.AddField(
            model_name='degree',
            name='picture',
            field=models.ImageField(blank=True, default='management/resource_img/default.jpg', height_field=500, max_length=225, null=True, upload_to='management/resource_img/', verbose_name='Picture', width_field=1000),
        ),
        migrations.AddField(
            model_name='degreecategory',
            name='picture',
            field=models.ImageField(blank=True, default='management/resource_img/default.jpg', height_field=500, max_length=225, null=True, upload_to='management/resource_img/', verbose_name='Picture', width_field=1000),
        ),
        migrations.AddField(
            model_name='module',
            name='picture',
            field=models.ImageField(blank=True, default='management/resource_img/default.jpg', height_field=500, max_length=225, null=True, upload_to='management/resource_img/', verbose_name='Picture', width_field=1000),
        ),
        migrations.AddField(
            model_name='modulelevel',
            name='picture',
            field=models.ImageField(blank=True, default='management/resource_img/default.jpg', height_field=500, max_length=225, null=True, upload_to='management/resource_img/', verbose_name='Picture', width_field=1000),
        ),
    ]
