# Generated by Django 5.0.1 on 2024-03-28 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='profile_img',
            field=models.ImageField(default='default.png', upload_to='patient_profile_images'),
        ),
    ]
