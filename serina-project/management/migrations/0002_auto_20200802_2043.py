# Generated by Django 3.0.8 on 2020-08-02 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='classroom',
            options={'ordering': ('name', 'reference'), 'verbose_name': 'Classroom', 'verbose_name_plural': 'Classrooms'},
        ),
        migrations.RemoveField(
            model_name='classroom',
            name='label',
        ),
        migrations.AddField(
            model_name='classroom',
            name='name',
            field=models.CharField(default='hello', max_length=50, verbose_name='Name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='classroom',
            name='reference',
            field=models.CharField(blank=True, max_length=7, unique=True, verbose_name='Reference'),
        ),
    ]