# Generated by Django 3.2.3 on 2022-03-10 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qrscan', '0006_delete_ticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='tickett',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
