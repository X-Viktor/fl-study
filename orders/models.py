from django.db import models

from authorization.models import User


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']


class Order(models.Model):
    STAGE_CHOICES = (
        (1, 'Открыто'),
        (2, 'Выполняется'),
        (3, 'Выполнено'),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category', verbose_name='Категория')
    title = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, verbose_name='Стоимость')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer', verbose_name='Заказчик')
    performer = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='performer', blank=True, null=True,
                                  verbose_name='Исполнитель')
    stage = models.PositiveSmallIntegerField(choices=STAGE_CHOICES, default=1, verbose_name='Состояние')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-date_creation']
