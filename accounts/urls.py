from django.urls import path,include
from .views import users_list


urlpatterns = [
    path("users/", users_list),
    path("signup/", include("dj_rest_auth.registration.urls")),
]