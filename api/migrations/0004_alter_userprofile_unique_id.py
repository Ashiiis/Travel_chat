# Generated by Django 5.1.1 on 2024-10-21 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_userprofile_unique_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='unique_id',
            field=models.AutoField(default=1001, primary_key=True, serialize=False),
        ),
    ]
