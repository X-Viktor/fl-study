from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from .forms import OrderCreateForm, ResponseForm
from .models import Order
from .services.order_detail import response_check


class MainView(ListView):
    """Отображение главной страницы."""
    model = Order
    context_object_name = 'orders'
    queryset = Order.objects.filter(stage=1).select_related('category')[:6]
    template_name = 'main.html'


class OrderListView(ListView):
    """Отображение всех заказов."""
    model = Order
    context_object_name = 'orders'
    queryset = Order.objects.filter(stage=1).select_related('category')
    extra_context = {'all_orders': True}
    template_name = 'orders/all-orders.html'

    paginate_by = 10


class OrderListByCategoryView(ListView):
    """Отображение заказов определенной категории."""
    model = Order
    context_object_name = 'orders'
    template_name = 'orders/all-orders.html'

    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(OrderListByCategoryView, self).get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']
        return context

    def get_queryset(self):
        return Order.objects.filter(category__slug=self.kwargs['slug'], stage=1).select_related('category')


class OrderDetailView(DetailView):
    """Отображение подробностей заказа."""
    model = Order
    context_object_name = 'order'
    template_name = 'orders/order-detail.html'

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context.update(response_check(self.request.user, kwargs['object']))
        return context

    def post(self, request, pk):
        form = ResponseForm(self.request.POST)
        if form.is_valid():
            if not self.request.user.is_authenticated:
                return redirect('signin')
            response = form.save(commit=False)
            response.order = Order.objects.get(pk=pk)
            response.responding = self.request.user
            response.save()
            return redirect('order_detail', pk=pk)
        return render(request, self.template_name, {'form': form})

    def get_object(self, queryset=None):
        return Order.objects.select_related('customer', 'performer').get(id=self.kwargs['pk'])


class OrderCreateView(LoginRequiredMixin, CreateView):
    """Создание нового заказа."""
    login_url = '/signin/'
    redirect_field_name = 'next'

    form_class = OrderCreateForm
    template_name = 'form.html'

    def form_valid(self, form):
        form.instance.customer = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Создание заказа'
        context['button_title'] = 'Создать'
        return context

    def get_success_url(self, **kwargs):
        return reverse('order_detail', kwargs={'pk': self.object.pk})


class OrderUpdateView(UpdateView):
    """Редактирование заказа."""
    form_class = OrderCreateForm
    template_name = 'form.html'

    def get_context_data(self, **kwargs):
        context = super(OrderUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Редактирование'
        context['button_title'] = 'Сохранить'
        return context

    def get_object(self, queryset=None):
        order = Order.objects.select_related('customer').get(id=self.kwargs['pk'])
        if (not order.customer == self.request.user) or (order.stage != 1):
            raise Http404
        return order

    def get_success_url(self, **kwargs):
        return reverse('order_detail', kwargs={'pk': self.object.pk})


class OrderDeleteView(DeleteView):
    """Удаление заказа."""
    model = Order
    success_url = reverse_lazy('orders')
    template_name = 'orders/order-delete.html'

    def get_object(self, queryset=None):
        order = Order.objects.select_related('customer').get(id=self.kwargs['pk'])
        if (not order.customer == self.request.user) or (order.stage != 1):
            raise Http404
        return order
