from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from .forms import OrderCreateForm, ResponseForm
from .models import Order, Response
from authorization.models import User


class MainView(ListView):
    """ Главная страница """
    model = Order
    template_name = 'main.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(stage=1).select_related('category')[:6]


class OrderListView(ListView):
    """ Вывод всех заказов """
    model = Order
    template_name = 'orders/all-orders.html'
    context_object_name = 'orders'

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        context['all_orders'] = True
        return context

    def get_queryset(self):
        return Order.objects.filter(stage=1).select_related('category')


class OrderDetailView(DetailView):
    """ Подробности заказа """
    model = Order
    context_object_name = 'order'
    template_name = 'orders/order-detail/base.html'

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['form'] = ResponseForm(self.request.POST or None)
        context['responses'] = Response.objects.filter(order__id=self.kwargs['pk']).select_related('responding')
        context['responding'] = User.objects.filter(responses__order__id=self.kwargs['pk'])
        return context

    def post(self, request, pk):
        form = ResponseForm(self.request.POST or None)
        if form.is_valid():
            if self.request.user.is_anonymous:
                return redirect('signin')
            response = form.save(commit=False)
            response.order = Order.objects.get(pk=pk)
            response.responding = self.request.user
            response.save()
            return redirect('order_detail', pk=pk)
        return render(request, self.template_name, {'form': form})

    def get_object(self, queryset=None):
        return Order.objects.select_related('customer', 'performer').get(id=self.kwargs['pk'])


class OrderUpdateView(UpdateView):
    """ Редактирование заказа """
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
    """ Удаление заказа """
    model = Order
    success_url = reverse_lazy('orders')
    template_name = 'orders/order-delete.html'

    def get_object(self, queryset=None):
        order = Order.objects.select_related('customer').get(id=self.kwargs['pk'])
        if (not order.customer == self.request.user) or (order.stage != 1):
            raise Http404
        return order


class OrderListByCategoryView(ListView):
    """ Вывод заказов определенной категории """
    model = Order
    template_name = 'orders/all-orders.html'
    context_object_name = 'orders'

    def get_context_data(self, **kwargs):
        context = super(OrderListByCategoryView, self).get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']
        return context

    def get_queryset(self):
        return Order.objects.filter(category__slug=self.kwargs['slug'], stage=1).select_related('category')


class OrderCreateView(CreateView):
    """ Создание нового заказа """
    form_class = OrderCreateForm
    template_name = 'form.html'

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Создание заказа'
        context['button_title'] = 'Создать'
        return context

    def get(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return redirect('signin')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            if self.request.user.is_anonymous:
                return redirect('signin')
            order = form.save(commit=False)
            order.customer = self.request.user
            order.save()
            return redirect('order_detail', pk=order.pk)
        return render(request, self.template_name, {'form': form})
