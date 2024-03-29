# Generated by Django 3.1.1 on 2020-10-17 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0003_merge_20201013_0655'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='store',
            name='closing_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='store',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='store',
            name='opening_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
