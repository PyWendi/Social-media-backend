from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token, RefreshToken

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import *
from django.contrib.auth import get_user_model

from datetime import timedelta

"""

TOken Serializer

"""

class CustomToken(Token):
    token_type = 'access'
    lifetime = timedelta(minutes=5)  # Set the token lifetime in seconds (5 minutes in this example)

    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        token['uid'] = user.uid
        return token
    
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': 'No active account found with the given email and password.',
        'other_problem': 'Bad Error'
    }
    email = serializers.EmailField(write_only=True)

    def validate(self, attrs):
        User = get_user_model()
        email = attrs.get('email')
        password = attrs.get('password')

        user = User.objects.get(email=email)

        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            access_token = CustomToken.for_user(user)
            return {
                'access': str(access_token),
                'refresh': str(refresh),
            }

        raise serializers.ValidationError('Invalid email or password')



""" 

User Serializer Class

"""

class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        User = get_user_model()
        model = User
        fields = ['fname', "lname", "email", "tel", "country", "date_of_birth", "password", "uid"]
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)
        if password :
            user.set_password(password)
        user.save()
        return user
        
class PageFollowedSerializer(ModelSerializer):
    class Meta:
        model = PageFollowed
        fields = "__all__"