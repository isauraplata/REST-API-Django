from django.urls import path
from employees import views

 
urlpatterns = [
    path('api/v1/employee/getAll/', views.getAll, name="get_employees"),
    path('api/v1/employee/create/', views.create_employee, name="create_employee"),
    path('api/v1/employee/delete/<int:employee_id>/',
         views.delete_employee, name="delete_employee"),
    path('api/v1/employee/update/<int:employee_id>/',
         views.update_employee, name="update_employee"),
]
