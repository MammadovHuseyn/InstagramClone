# Generated by Django 4.2 on 2023-04-09 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_rename_about_profile_bio_story'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='image',
        ),
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='/User_Image/default-user.png', upload_to='User_Image'),
        ),
    ]
