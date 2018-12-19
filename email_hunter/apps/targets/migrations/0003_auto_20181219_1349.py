# Generated by Django 2.0.9 on 2018-12-19 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('targets', '0002_targetfile_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='targetfile',
            name='file',
        ),
        migrations.AddField(
            model_name='targetfile',
            name='filename',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
