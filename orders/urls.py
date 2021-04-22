from django.urls import path

from . import views

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('category/<slug:slug>/', views.OrderListByCategoryView.as_view(), name='category'),
    path('create_order/', views.OrderCreateView.as_view(), name='create_order'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('order/<int:pk>/edit', views.OrderUpdateView.as_view(), name='order_edit'),
    path('order/<int:pk>/delete', views.OrderDeleteView.as_view(), name='order_delete'),
]