# Generated by Django 4.1.7 on 2023-03-16 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0004_alter_item_description_alter_item_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='video_link',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]
