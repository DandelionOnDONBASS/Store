from django.urls import path
from django.views.decorators.cache import cache_page

from orders.views import OrderCreateView, OrderDetailView, OrderListView

app_name = 'orders'

urlpatterns = [
    path('order-create/', OrderCreateView.as_view(), name='order_create'),
    path('', OrderListView.as_view(), name='order_list'),
    path('order/<int:pk>', OrderDetailView.as_view(), name='order'),
]

