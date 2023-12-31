# Generated by Django 4.2.2 on 2023-06-16 16:54

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0003_alter_orders_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 16, 22, 24, 16, 239500)),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('selling_price', models.IntegerField()),
                ('transaction_date', models.DateTimeField(default=datetime.datetime(2023, 6, 16, 22, 24, 16, 239500))),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Inventory.inventory')),
            ],
        ),
    ]
