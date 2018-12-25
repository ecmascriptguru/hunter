# Generated by Django 2.0.9 on 2018-12-25 03:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
        ('targets', '0003_auto_20181219_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='target',
            name='job',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='targets', to='jobs.Job'),
        ),
        migrations.AlterUniqueTogether(
            name='target',
            unique_together={('first_name', 'last_name', 'domain')},
        ),
    ]
