from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("dj_rest_auth.urls")),
    path('accounts/',include('accounts.urls')),
    #path("trip/", include("trip.urls")),
    #path("vehicle/", include("vehicle.urls")),
    #path("lostfound/", include("lostfound.urls")),
]
