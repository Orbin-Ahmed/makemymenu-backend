# Generated by Django 4.1.7 on 2023-03-12 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0005_alter_branch_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='placeholder_item',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='branch',
            name='placeholder_meals',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
