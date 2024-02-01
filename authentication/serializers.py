from .exceptions import ExternalAPIError
from rest_framework import serializers
from .models import *
import requests
from django.core.validators import RegexValidator
import os

class UserProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = User_Profile
        fields = ['image']

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = serializers.CharField(validators=[phone_regex], max_length=17, required=False)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'username', 'id']

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'phone_number','program', 'course')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(user.password)
        user.is_active = False
        user.save()
        message = f"Hello {user.username}, Welcome to Dreamosoft."
        data = {
        'expiry': 5,
        'length': 6,
        'medium': 'sms',
        'message': message+' This is your verification code:\n%otp_code%\nPlease do not share this code with anyone.',
        'number': user.phone_number,
        'sender_id': 'Drmosft',
        'type': 'numeric',
        }

        headers = {
        'api-key': os.environ.get('ARK_API_KEY'),
        }

        url = 'https://sms.arkesel.com/api/otp/generate'

        try:
            response = requests.post(url, json=data, headers=headers)
            if response.status_code != 200:
                user.delete()
                raise ExternalAPIError(response.status_code, response.json())
        except requests.RequestException as e:
            user.delete()
            raise ExternalAPIError(500, str(e))
        
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class FullUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(source='user_profile')
    
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'email', 'phone_number', 'profile', 'username']

class UserResendOtpSerializer(serializers.Serializer):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = serializers.CharField(validators=[phone_regex], max_length=17, required=True)
    user_id = serializers.CharField()

class VerifyUserPinSerializer(serializers.Serializer):
    pin = serializers.CharField(max_length=5)

class UserOtpVerificationSerializer(serializers.Serializer):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    code = serializers.CharField()
    user_id = serializers.CharField()
    phone = serializers.CharField(validators=[phone_regex], max_length=17, required=True)