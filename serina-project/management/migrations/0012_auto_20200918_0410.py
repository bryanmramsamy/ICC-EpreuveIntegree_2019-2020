# Generated by Django 3.1.1 on 2020-09-18 02:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0011_auto_20200914_0357'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='picture',
        ),
        migrations.AlterField(
            model_name='classroom',
            name='description',
            field=models.TextField(blank=True, help_text='Should provide as much information on the module as possible.', null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='classroom',
            name='max_capacity',
            field=models.PositiveIntegerField(help_text='Maximal capacity in case of over attendance.', verbose_name='Maximum capacity'),
        ),
        migrations.AlterField(
            model_name='classroom',
            name='name',
            field=models.CharField(help_text='Must be as short and descriptive as possible.', max_length=50, verbose_name='Designation'),
        ),
        migrations.AlterField(
            model_name='classroom',
            name='picture',
            field=models.ImageField(blank=True, default='management/books.png', help_text='Not required. If no picture is sent, the default picture will be used.', max_length=225, null=True, upload_to='management/rooms/', verbose_name='Picture'),
        ),
        migrations.AlterField(
            model_name='classroom',
            name='recommended_capacity',
            field=models.PositiveIntegerField(help_text='Capacity where the attendees can work in optimal conditions.', verbose_name='Recommended capacity'),
        ),
        migrations.AlterField(
            model_name='degree',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='degrees', to='management.degreecategory', verbose_name='Degree category'),
        ),
        migrations.AlterField(
            model_name='degree',
            name='description',
            field=models.TextField(blank=True, help_text='Should provide as much information on the module as possible.', null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='degree',
            name='modules',
            field=models.ManyToManyField(help_text='All the modules which are part of the degree.', related_name='degrees', to='management.Module', verbose_name='Modules'),
        ),
        migrations.AlterField(
            model_name='degree',
            name='picture',
            field=models.ImageField(blank=True, default='management/books.png', help_text='Not required. If no picture is sent, the default picture will be used.', max_length=225, null=True, upload_to='management/degrees/', verbose_name='Picture'),
        ),
        migrations.AlterField(
            model_name='degree',
            name='title',
            field=models.CharField(help_text="To avoid confusion, it's recommended to use different names for each degree.", max_length=255, verbose_name='Degree name'),
        ),
        migrations.AlterField(
            model_name='degreecategory',
            name='name',
            field=models.CharField(help_text="An explicite name is recommended, such as 'Bachelor', 'PhD', or 'Master'. ", max_length=50, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='module',
            name='ECTS_value',
            field=models.PositiveIntegerField(blank=True, help_text='Cannot be negative.', null=True, verbose_name='ECTS value'),
        ),
        migrations.AlterField(
            model_name='module',
            name='cost',
            field=models.DecimalField(decimal_places=2, help_text='Cannot be negative.', max_digits=5, null=True, verbose_name='Cost per student'),
        ),
        migrations.AlterField(
            model_name='module',
            name='description',
            field=models.TextField(blank=True, help_text='Should provide as much information on the module as possible.', null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='module',
            name='level',
            field=models.ForeignKey(help_text="Rank the module by it's diffictuly.", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modules', to='management.modulelevel', verbose_name='Difficulty level'),
        ),
        migrations.AlterField(
            model_name='module',
            name='picture',
            field=models.ImageField(blank=True, default='management/books.png', help_text='Not required. If no picture is sent, the default picture will be used.', max_length=225, null=True, upload_to='management/modules/', verbose_name='Picture'),
        ),
        migrations.AlterField(
            model_name='module',
            name='price',
            field=models.DecimalField(decimal_places=2, help_text='Cannot be negative.', max_digits=5, null=True, verbose_name='Student charge price'),
        ),
        migrations.AlterField(
            model_name='module',
            name='title',
            field=models.CharField(help_text="To avoid confusion, it's recommended to use different names for each modules.", max_length=255, verbose_name='Module name'),
        ),
        migrations.AlterField(
            model_name='modulelevel',
            name='name',
            field=models.CharField(help_text="An explicite name is recommended, such as 'Beginner' or 'Intermediate'.", max_length=50, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='modulelevel',
            name='rank',
            field=models.PositiveIntegerField(help_text='Each level must have a unique rank. The higer the rank, the harder the difficulty level.', unique=True, verbose_name='Rank'),
        ),
    ]
