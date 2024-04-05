from django.urls import path
from menu import views

# url for menu

urlpatterns = [
    path('api/v1/menu/getAll/', views.get_menu, name="get_menu"),
    path('api/v1/menu/create/', views.create_dish, name="create_dish"),
    path('api/v1/menu/delete/<int:dish_id>/',
         views.delete_dish, name="delete_dish"),
    path('api/v1/menu/update/<int:dish_id>/',
         views.update_dish, name="update_dish"),
]
