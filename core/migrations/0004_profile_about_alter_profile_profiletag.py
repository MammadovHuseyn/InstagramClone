# Generated by Django 4.2 on 2023-04-07 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_profile_profiletag'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='about',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profiletag',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
