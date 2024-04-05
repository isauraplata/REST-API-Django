from django.urls import path, include
from paypal_integration import views


urlpatterns = [
 path('purchase/', views.order_purchase, name='purchase'),
 path('paypal/', include("paypal.standard.ipn.urls")),
]
