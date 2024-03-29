# Generated by Django 4.1.7 on 2023-03-04 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('QR', models.ImageField(blank=True, null=True, upload_to='MenuQR/')),
                ('Wifi', models.ImageField(blank=True, null=True, upload_to='MenuQR/')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
