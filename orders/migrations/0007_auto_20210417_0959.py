# Generated by Django 3.1.7 on 2021-04-17 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20210417_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='response',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='orders.order', verbose_name='Заказ'),
        ),
    ]
