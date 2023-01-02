from django.urls import path
from . import views 

urlpatterns = [
    path("api/login/",views.Login.as_view()),
    path("api/home/",views.user_home.as_view(),name="home"),
    path("api/logout/",views.user_logout.as_view(),name="logout"),

]