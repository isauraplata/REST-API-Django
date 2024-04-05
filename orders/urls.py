from django.urls import path, re_path
from orders import views

# url for orders
 
urlpatterns = [
    path('api/v1/order/getAll/', views.get_orders, name="get_orders"),
    path('api/v1/order/create/', views.create_order, name="create_order"),
    path('api/v1/order/delete/<int:order_id>/',
         views.delete_order, name="delete_order"),
    path('api/v1/order/update/<int:order_id>/',
         views.update_order, name="update_order"),
    path('api/v1/order/get/<int:order_id>/',
         views.get_order_by_id, name="get_order_by_id"),
]



