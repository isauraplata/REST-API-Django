from django.urls import path, re_path
from reservations import views

# url for reservations
 
urlpatterns = [
    path('api/v1/reservations/getAll/', views.getAll, name="getAll"),
    path('api/v1/reservations/create/',
         views.create_reservations, name="create_reservations"),
    path('api/v1/reservations/delete/<int:reservation_id>/',
         views.delete_reservation, name="delete_reservation"),
    path('api/v1/reservations/update/<int:reservation_id>/',
         views.update_reservation, name="update_reservation"),
]
