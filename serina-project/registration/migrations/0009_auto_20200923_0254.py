# Generated by Django 3.1.1 on 2020-09-23 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0008_moduleregistrationreport_exemption_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentregistrationreport',
            name='student_is_foreigner',
            field=models.BooleanField(default=False, verbose_name='Foreign student'),
        ),
        migrations.AlterField(
            model_name='moduleregistrationreport',
            name='exemption_report',
            field=models.FileField(blank=True, help_text='Send the documents that can provide you a exemption for this module. The documents will be verified by our staff and help them taking a decision regarding your request.', null=True, upload_to='', verbose_name='Exemption reports'),
        ),
        migrations.AlterField(
            model_name='moduleregistrationreport',
            name='exemption_request',
            field=models.BooleanField(default=False, help_text='If you already succeeded this or a similar module in another school or educational organization, you can ask for an exemption. This will prevent you from passing paying this module if your request is accepted by our staff.', verbose_name='Student exemption request'),
        ),
    ]