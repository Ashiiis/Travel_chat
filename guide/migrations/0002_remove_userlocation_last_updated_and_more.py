# Generated by Django 5.1.1 on 2024-10-22 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guide', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userlocation',
            name='last_updated',
        ),
        migrations.RemoveField(
            model_name='userlocation',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='userlocation',
            name='longitude',
        ),
        migrations.AlterField(
            model_name='userlocation',
            name='city',
            field=models.CharField(max_length=255),
        ),
    ]