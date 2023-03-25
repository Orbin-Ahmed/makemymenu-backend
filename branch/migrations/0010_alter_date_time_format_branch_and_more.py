# Generated by Django 4.1.7 on 2023-03-15 07:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0009_notification_settings_localization_date_time_format'),
    ]

    operations = [
        migrations.AlterField(
            model_name='date_time_format',
            name='branch',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='branch.branch'),
        ),
        migrations.AlterField(
            model_name='localization',
            name='branch',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='branch.branch'),
        ),
        migrations.AlterField(
            model_name='notification_settings',
            name='branch',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='branch.branch'),
        ),
    ]