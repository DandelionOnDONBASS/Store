from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from orders.forms import OrderForm
from orders.models import Order
from store.common.views import TitleMixin


class SuccessTemplateView(TitleMixin,TemplateView):
    template_name = 'orders/success.html'
    title = 'Store - Спасибо за заказ!'

class OrderListView(TitleMixin, ListView):
    template_name = 'orders/orders.html'
    title = 'Store - Заказы'
    queryset = Order.objects.all()
    ordering = ('-id')

    def get_queryset(self):
        quaryset = super(OrderListView, self).get_queryset()
        return quaryset.filter(initiator = self.request.user)


class OrderDetailView(TitleMixin, DetailView):
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['title'] = f'Store - Заказ № {self.object.id}'
        return context

class OrderCreateView(TitleMixin ,CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    # success_url = reverse_lazy('orders:order_create')
    title = 'Store - Оформление заказа'

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        response =  super(OrderCreateView, self).form_valid(form)
        self.object.update_after_payment()

        return response

    def get_success_url(self):
        return reverse_lazy('users:profile',args=(self.object.initiator.id,))


