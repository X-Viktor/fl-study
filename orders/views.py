from django.views.generic import ListView

from .models import Order


class OrderListView(ListView):
    """ Вывод всех заказов """
    model = Order
    template_name = 'orders/main.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(stage=1).select_related('category')


class OrderListByCategoryView(ListView):
    """ Вывод заказов определенной категории """
    model = Order
    template_name = 'orders/main.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(category__slug=self.kwargs['slug'], stage=1).select_related('category')
