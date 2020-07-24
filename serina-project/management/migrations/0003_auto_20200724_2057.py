# Generated by Django 3.0.8 on 2020-07-24 18:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('management', '0002_auto_20200724_2025'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='curriculum',
            options={'ordering': ('-date_updated', '-date_created', 'title'), 'verbose_name': 'Curriculum', 'verbose_name_plural': 'Curriculums'},
        ),
        migrations.RemoveField(
            model_name='curriculum',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='module',
            name='date_end',
        ),
        migrations.RemoveField(
            model_name='module',
            name='date_start',
        ),
        migrations.RemoveField(
            model_name='module',
            name='student',
        ),
        migrations.RemoveField(
            model_name='module',
            name='teachers',
        ),
        migrations.AddField(
            model_name='curriculum',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='curriculum',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Created on'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='curriculum',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated on'),
        ),
        migrations.AddField(
            model_name='curriculum',
            name='modules',
            field=models.ManyToManyField(related_name='module_curricula', to='management.Module', verbose_name='Curricula'),
        ),
    ]