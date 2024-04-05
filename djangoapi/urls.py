from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    # url for Auth
    path('', include('authentication.urls')),
    # url for Employee
     path('', include('employees.urls')),
    # url for Reservations
    path('', include('reservations.urls')),
    # url for Menu
    path('', include('menu.urls')),
    # url for Employee
     path('', include('employees.urls')),
    # url for paypal
    path('', include('paypal_integration.urls')),
]
