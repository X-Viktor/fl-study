# Generated by Django 3.1.7 on 2021-04-17 09:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0005_auto_20210408_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации'),
        ),
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True, verbose_name='Вознаграждение'),
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='Сообщение')),
                ('date_response', models.DateTimeField(auto_now_add=True, verbose_name='Дата отклика')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='orders.order', verbose_name='Заказ')),
                ('responding', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responding', to=settings.AUTH_USER_MODEL, verbose_name='Откликнувшийся')),
            ],
            options={
                'verbose_name': 'Отклик',
                'verbose_name_plural': 'Отклики',
                'ordering': ['-date_response'],
            },
        ),
    ]
