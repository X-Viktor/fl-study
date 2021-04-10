from django.urls import path

from .views import OrderListView, OrderListByCategoryView

urlpatterns = [
    path('', OrderListView.as_view(), name='main'),
    path('category/<slug:slug>/', OrderListByCategoryView.as_view(), name='category')
]