# Generated by Django 3.1.1 on 2020-11-23 06:57

import accounts.helpers
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20201108_0323'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cuisine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, unique=True)),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, default='products/cuisine/image/default.png', height_field='height_field', null=True, upload_to=accounts.helpers.UploadTo('image'), width_field='width_field')),
                ('height_field', models.IntegerField(default=0, null=True)),
                ('width_field', models.IntegerField(default=0, null=True)),
                ('active', models.BooleanField(default=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'cuisine',
                'verbose_name_plural': 'cuisines',
            },
        ),
    ]
