# Generated by Django 4.2 on 2023-05-14 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_remove_customuser_favorites_favorite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favorite',
            name='posts',
        ),
        migrations.AddField(
            model_name='favorite',
            name='post',
            field=models.ManyToManyField(related_name='post_favorites', to='core.posts'),
        ),
    ]
