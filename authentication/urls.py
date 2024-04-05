from django.urls import path, re_path
from authentication import views

# url for Auth
 
urlpatterns = [
     
    path('api/v1/signup/', views.signup, name="signup"),
    path('api/v1/signin/', views.signin, name="signin"),
    path('api/v1/logout/', views.signout, name="logout"),
]
