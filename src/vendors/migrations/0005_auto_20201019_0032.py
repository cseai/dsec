# Generated by Django 3.1.1 on 2020-10-18 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0004_auto_20201018_0039'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='store',
            name='tagline',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='store',
            name='username',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='store',
            name='category',
            field=models.CharField(choices=[('', 'Select store category'), ('C', 'Company'), ('P', 'Personal'), ('O', 'Other')], max_length=20),
        ),
    ]
