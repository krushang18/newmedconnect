# Generated by Django 5.0.1 on 2024-03-28 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_patient_profile_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='profile_img',
            field=models.ImageField(default='doctors_profile_images/default.png', upload_to='doctors_profile_images'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='profile_img',
            field=models.ImageField(default='patient_profile_images/default.png', upload_to='patient_profile_images'),
        ),
    ]