from django.views.generic import ListView

from .models import Order


class OrderListView(ListView):
    model = Order
    template_name = 'orders/main.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(stage=1).select_related('category')
