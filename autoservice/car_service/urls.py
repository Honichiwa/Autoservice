from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name="index"),
    path('car_list/', views.car_list, name='car_list'),
    path('car_list/<int:pk>/', views.car_detail, name='car_detail'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/my/', views.UserOrderList.as_view(), name='user_order_list'),
    path('car_list/my/', views.UserCarList.as_view(), name='user_car_list'),
    path('car_list/car_create/', views.CarCreateView.as_view(), name='car_create'),
    path('order_list/order_create/', views.OrderCreateView.as_view(), name='order_create'),
    path('order_list/new/', views.UserOrderCreateView.as_view(), name='user_order_create'),
    path('car_list/my/update/<int:pk>/', views.CarUpdateView.as_view(), name='car_update'),
    path('car_list/my/delete/<int:pk>/', views.CarDeleteView.as_view(), name='car_delete'),
    path('orders/my/delete/<int:pk>/', views.UserOrderDeleteView.as_view(), name='order_delete'),

]