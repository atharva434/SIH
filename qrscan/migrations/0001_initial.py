# Generated by Django 2.2 on 2022-03-09 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket_booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=20)),
                ('monument', models.CharField(max_length=20)),
                ('date', models.DateField()),
                ('email', models.EmailField(max_length=254)),
                ('count', models.IntegerField()),
                ('ticket_price', models.DecimalField(decimal_places=1, max_digits=7)),
                ('total_cost', models.CharField(max_length=20)),
                ('status', models.CharField(default='Pending', max_length=254, verbose_name='Payment Status')),
                ('provider_order_id', models.CharField(max_length=40, verbose_name='Order ID')),
                ('payment_id', models.CharField(max_length=36, verbose_name='Payment ID')),
                ('signature_id', models.CharField(max_length=128, verbose_name='Signature ID')),
            ],
        ),
    ]