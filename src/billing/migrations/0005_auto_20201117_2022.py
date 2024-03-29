# Generated by Django 3.1.1 on 2020-11-17 14:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20201108_0323'),
        ('vendors', '0010_merge_20201109_2148'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('express', '0003_auto_20201115_0225'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('billing', '0004_auto_20201108_0323'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='storeordertrx',
            options={'ordering': ['-timestamp']},
        ),
        migrations.AlterModelOptions(
            name='vendoradmintrx',
            options={'ordering': ['-timestamp']},
        ),
        migrations.RemoveField(
            model_name='storeordertrx',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='vendoradmintrx',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='vendoradmintrx',
            name='vouchar_amount',
        ),
        migrations.AddField(
            model_name='storeordertrx',
            name='content_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='storeordertrx',
            name='message',
            field=models.CharField(blank=True, editable=False, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='storeordertrx',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='vendoradmintrx',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0.0, editable=False, max_digits=20),
        ),
        migrations.AddField(
            model_name='vendoradmintrx',
            name='content_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='vendoradmintrx',
            name='message',
            field=models.CharField(blank=True, editable=False, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='vendoradmintrx',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='storeordertrx',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0.0, editable=False, max_digits=20),
        ),
        migrations.AlterField(
            model_name='storeordertrx',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sot_order', to='orders.order'),
        ),
        migrations.AlterField(
            model_name='storeordertrx',
            name='store',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sot_store', to='vendors.store'),
        ),
        migrations.AlterField(
            model_name='vendoradmintrx',
            name='admin_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vat_admin_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='vendoradmintrx',
            name='store',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vat_store', to='vendors.store'),
        ),
        migrations.AlterField(
            model_name='vendoradmintrx',
            name='vendor_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vat_vendor_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='MerchantAdminTrx',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, editable=False, max_digits=20)),
                ('message', models.CharField(blank=True, editable=False, max_length=200, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('admin_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mat_admin_user', to=settings.AUTH_USER_MODEL)),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype')),
                ('merchant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mat_merchant', to='express.merchant')),
                ('merchant_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mat_merchant_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
