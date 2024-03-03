from django.contrib import admin
from django.urls import path
from reservations import views as reservations_views
from menu import views as menu_views
from employees import views as employees_views
from orders import views as orders_views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # url for Auth
    path('api/v1/signup/', reservations_views.signup, name="signup"),
    path('api/v1/signin/', reservations_views.signin, name="signin"),
    path('api/v1/logout/', reservations_views.signout, name="logout"),
    # url for Reservations
    path('api/v1/reservations/getAll/', reservations_views.getAll, name="getAll"),
    path('api/v1/reservations/create/',
         reservations_views.create_reservations, name="create_reservations"),
    path('api/v1/reservations/delete/<int:reservation_id>/',
         reservations_views.delete_reservation, name="delete_reservation"),
    path('api/v1/reservations/update/<int:reservation_id>/',
         reservations_views.update_reservation, name="update_reservation"),
    # url for Menu
    path('api/v1/menu/getAll/', menu_views.get_menu, name="get_menu"),
    path('api/v1/menu/create/', menu_views.create_dish, name="create_dish"),
    path('api/v1/menu/delete/<int:dish_id>/',
         menu_views.delete_dish, name="delete_dish"),
    path('api/v1/menu/update/<int:dish_id>/',
         menu_views.update_dish, name="update_dish"),
    # url for Order
    path('api/v1/order/getAll/', orders_views.get_orders, name="get_orders"),
    path('api/v1/order/create/', orders_views.create_order, name="create_order"),
    path('api/v1/order/delete/<int:order_id>/',
         orders_views.delete_order, name="delete_order"),
    path('api/v1/order/update/<int:order_id>/',
         orders_views.update_order, name="update_order"),
    # url for Employee
    path('api/v1/employee/getAll/', employees_views.getAll, name="get_employees"),
    path('api/v1/employee/create/', employees_views.create_employee, name="create_employee"),
    path('api/v1/employee/delete/<int:employee_id>/',
         employees_views.delete_employee, name="delete_employee"),
    path('api/v1/employee/update/<int:employee_id>/',
         employees_views.update_employee, name="update_employee"),

]
