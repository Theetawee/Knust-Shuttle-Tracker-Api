from django.urls import path
from .views import *

urlpatterns = [
    path('get-user-token/', get_user_token, name="get_token"),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('verify/', UserOtpVerification.as_view(), name='verify'),
    path('update/user/', UserUpdateView.as_view(), name='user-update'),
    path('user/', UserListView.as_view(), name='user-list'),
    path('profile/', UserProfileUpdateView.as_view(), name='profile-update'),
    path('resend-otp/', UserResendOTP.as_view(), name='resend-otp'),
]