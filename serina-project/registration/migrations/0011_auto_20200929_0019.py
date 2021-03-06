# Generated by Django 3.1.1 on 2020-09-28 22:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0010_auto_20200926_0057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='degreeregistrationreport',
            name='exemption_report',
            field=models.FileField(blank=True, help_text='Send the documents that can provide you a exemption for one or miltiple modules of this degree. The documents will be verified by our staff and help them taking a decision regarding your request.', null=True, upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'zip', 'jpeg', 'jpg', 'png'])], verbose_name='Exemption reports'),
        ),
        migrations.AlterField(
            model_name='degreeregistrationreport',
            name='exemption_request',
            field=models.BooleanField(default=False, help_text='If you already succeeded this or a similar module part of this degree in another school or educational organization, you can ask for an exemption. This will prevent you from passing paying this module if your request is accepted by our staff.', verbose_name='Student exemption request'),
        ),
    ]
