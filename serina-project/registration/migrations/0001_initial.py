# Generated by Django 3.0.8 on 2020-08-01 18:03

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('management', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DegreeRegistrationReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Updated on')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Additional notes')),
                ('date_start', models.DateField(verbose_name='Start date')),
                ('date_end', models.DateField(verbose_name='End date')),
                ('degree', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students_registrations', to='management.Degree', verbose_name='Registration degree')),
            ],
            options={
                'verbose_name': 'Degree Registration Report',
                'verbose_name_plural': 'Degrees Registration Reports',
            },
        ),
        migrations.CreateModel(
            name='StudentRegistrationReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Updated on')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Additional notes')),
                ('birthday', models.DateField(verbose_name='Birthday date')),
                ('nationality', models.CharField(max_length=50, verbose_name='Nationality')),
                ('address', models.CharField(max_length=255, verbose_name='Address')),
                ('additional_address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Additional address')),
                ('postal_code', models.CharField(max_length=50, verbose_name='Postal code')),
                ('postal_locality', models.CharField(max_length=50, verbose_name='Locality')),
                ('id_picture', models.ImageField(upload_to='', verbose_name='ID picture')),
                ('id_card', models.FileField(upload_to='', verbose_name='ID card')),
                ('secondary_education_certificate', models.FileField(upload_to='', verbose_name='Secondary Education Certificate')),
                ('annex_403', models.FileField(blank=True, null=True, upload_to='', verbose_name='Annex 403')),
                ('other_school_inscription_certificate', models.FileField(blank=True, null=True, upload_to='', verbose_name='Other schools inscription certificate')),
                ('national_register_extract', models.FileField(blank=True, null=True, upload_to='', verbose_name='National Register Extract')),
                ('belgian_studies_history', models.FileField(blank=True, null=True, upload_to='', verbose_name='Belgian Studies History')),
                ('archievement_certificates', models.FileField(blank=True, null=True, upload_to='', verbose_name='Modules archievement certificates')),
                ('job_organization_certificates', models.FileField(blank=True, null=True, upload_to='', verbose_name='Job organizations certificates')),
                ('exemption_report', models.FileField(blank=True, null=True, upload_to='', verbose_name='Exemption reports')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student_rr', to=settings.AUTH_USER_MODEL, verbose_name='Student')),
            ],
            options={
                'verbose_name': 'Student registration report',
                'verbose_name_plural': 'Student registration reports',
            },
        ),
        migrations.CreateModel(
            name='ModuleRegistrationReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Updated on')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Additional notes')),
                ('date_start', models.DateField(verbose_name='Start date')),
                ('date_end', models.DateField(verbose_name='End date')),
                ('student_attempt', models.PositiveIntegerField(default=0, verbose_name="Student's attempt number")),
                ('student_final_score', models.FloatField(default=-1, validators=[django.core.validators.MinValueValidator(-1), django.core.validators.MaxValueValidator(100)], verbose_name='Final score')),
                ('approved', models.BooleanField(default=False, verbose_name='Approved')),
                ('payed', models.BooleanField(default=False, verbose_name='Payed')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students_registrations', to='management.Course', verbose_name='Course')),
                ('degree_rr', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modules_rrs', to='registration.DegreeRegistrationReport', verbose_name='Degree Registration Report')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students_registrations', to='management.Module', verbose_name='Registration module')),
                ('student_rr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modules_rrs', to='registration.StudentRegistrationReport', verbose_name='Student')),
            ],
            options={
                'verbose_name': 'Module Registration Report',
                'verbose_name_plural': 'Modules Registration Reports',
            },
        ),
        migrations.AddField(
            model_name='degreeregistrationreport',
            name='student_rr',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='degrees_rrs', to='registration.StudentRegistrationReport', verbose_name='Student'),
        ),
    ]
