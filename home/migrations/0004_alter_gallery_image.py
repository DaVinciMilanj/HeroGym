# Generated by Django 5.1.3 on 2024-11-29 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_gallery_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='image',
            field=models.ImageField(upload_to='gallery'),
        ),
    ]
