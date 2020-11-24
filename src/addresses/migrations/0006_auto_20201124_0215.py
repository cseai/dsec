# Generated by Django 3.1.1 on 2020-11-23 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0005_auto_20201110_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(choices=[(None, 'Select City'), ('Barishal Division', (('Barguna', 'Barguna'), ('Barishal', 'Barishal'), ('Bhola', 'Bhola'), ('Jhalakathi', 'Jhalakathi'), ('Patuakhali', 'Patuakhali'), ('Pirojpur', 'Pirojpur'))), ('Chattogram Division', (('Bandarban', 'Bandarban'), ('Brahmanbaria', 'Brahmanbaria'), ('Chandpur', 'Chandpur'), ('Chattogram', 'Chattogram'), ('Cumilla', 'Cumilla'), ("Cox's Bazar", "Cox's Bazar"), ('Feni', 'Feni'), ('Khagrachhari', 'Khagrachhari'), ('Lakshmipur', 'Lakshmipur'), ('Noakhali', 'Noakhali'), ('Rangamati', 'Rangamati'))), ('Dhaka Division', (('Dhaka', 'Dhaka'), ('Faridpur', 'Faridpur'), ('Gazipur', 'Gazipur'), ('Gopalganj', 'Gopalganj'), ('Kishoreganj', 'Kishoreganj'), ('Madaripur', 'Madaripur'), ('Manikganj', 'Manikganj'), ('Munshiganj', 'Munshiganj'), ('Narayanganj', 'Narayanganj'), ('Narsingdi', 'Narsingdi'), ('Rajbari', 'Rajbari'), ('Shariatpur', 'Shariatpur'), ('Tangail', 'Tangail'))), ('Khulna Division', (('Bagerhat', 'Bagerhat'), ('Chuadanga', 'Chuadanga'), ('Jashore', 'Jashore'), ('Jhenaidah', 'Jhenaidah'), ('Khulna', 'Khulna'), ('Kushtia', 'Kushtia'), ('Magura', 'Magura'), ('Meherpur', 'Meherpur'), ('Narail', 'Narail'), ('Satkhira', 'Satkhira'))), ('Mymensingh Division', (('Jamalpur', 'Jamalpur'), ('Mymensingh', 'Mymensingh'), ('Netrokona', 'Netrokona'), ('Sherpur', 'Sherpur'))), ('Rajshahi Division', (('Bogura', 'Bogura'), ('Joypurhat', 'Joypurhat'), ('Naogaon', 'Naogaon'), ('Natore', 'Natore'), ('Nawabganj', 'Nawabganj'), ('Pabna', 'Pabna'), ('Rajshahi', 'Rajshahi'), ('Sirajganj', 'Sirajganj'))), ('Rangpur Division', (('Dinajpur', 'Dinajpur'), ('Gaibandha', 'Gaibandha'), ('Kurigram', 'Kurigram'), ('Lalmonirhat', 'Lalmonirhat'), ('Nilphamari', 'Nilphamari'), ('Panchagarh', 'Panchagarh'), ('Rangpur', 'Rangpur'), ('Thakurgaon', 'Thakurgaon'))), ('Sylhet Division', (('Habiganj', 'Habiganj'), ('Moulvibazar', 'Moulvibazar'), ('Sunamganj', 'Sunamganj'), ('Sylhet', 'Sylhet')))], max_length=20),
        ),
        migrations.AlterField(
            model_name='address',
            name='state',
            field=models.CharField(choices=[(None, 'Select State/Division'), ('Barishal', 'Barishal'), ('Chattogram', 'Chattogram'), ('Dhaka', 'Dhaka'), ('Khulna', 'Khulna'), ('Mymensingh', 'Mymensingh'), ('Rajshahi', 'Rajshahi'), ('Rangpur', 'Rangpur'), ('Sylhet', 'Sylhet')], max_length=20),
        ),
    ]
