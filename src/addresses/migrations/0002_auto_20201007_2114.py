# Generated by Django 3.1.1 on 2020-10-07 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'verbose_name': 'address', 'verbose_name_plural': 'addresses'},
        ),
    ]
