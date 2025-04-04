# Generated by Django 5.1.5 on 2025-03-20 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lost_cat', '0013_lostcat_lost_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='sightingreport',
            name='lost_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sightingreport',
            name='lost_location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='sightingreport',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='photos/'),
        ),
        migrations.AddField(
            model_name='sightingreport',
            name='photo2',
            field=models.ImageField(blank=True, null=True, upload_to='photos/'),
        ),
        migrations.AddField(
            model_name='sightingreport',
            name='photo3',
            field=models.ImageField(blank=True, null=True, upload_to='photos/'),
        ),
        migrations.AlterField(
            model_name='sightingreport',
            name='situation',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
    ]
