# Generated by Django 3.1.1 on 2020-11-14 20:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('express', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchant',
            name='payment_account_object_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='merchant',
            name='payment_account_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
    ]
