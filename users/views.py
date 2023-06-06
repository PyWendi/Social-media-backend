# Rest framework common import
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status

# TOKEN VIEW
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import Token, RefreshToken

# MODELS
from .models import CustomUser
from django.contrib.auth import get_user_model

# Import Token Serializer
from .serializers import (
    MyTokenObtainPairSerializer,
    UserSerializer,
    PageFollowedSerializer,
    CustomToken,
)

# Token generic getter view
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access = CustomToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(access),
        })


@api_view(['POST'])
def check_refresh_token_lifetime(token):
    refresh_token = RefreshToken(token)
    remaining_lifetime = refresh_token.lifetime.total_seconds()
    return remaining_lifetime
    
@api_view(["GET"])
def getRoutes(request):
    routes = [
        '/api/user/token',
        '/api/user/token/refresh',
        '/api/user/token/verify',
        'token/lifetime/',
    ]

    return Response(routes)


@api_view(['POST'])
def getLifetime(request):
    refresh = request.POST.get("refresh")
    refresh_lifetime = check_refresh_token_lifetime(refresh)
    return Response(refresh_lifetime)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def pageFollowed(request):
    user = get_user_model()
    User = user.objects.get(username="zodiak")
    follow = User.pagefollowed_set.all()

    if follow:
        serializer = PageFollowedSerializer(follow, many=True)
        return Response(serializer.data)
    else :
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(["GET"])
def getUsers(request):
    user = get_user_model()
    Users = user.objects.all()
    serializer = UserSerializer(Users, many=True)
    return Response(serializer.data)
    
@api_view(["GET"])
def getUser(request, pk):
    user = get_user_model()
    Users = user.objects.get(pk=pk)
    serializer = UserSerializer(Users)
    return Response(serializer.data)



@api_view(["PUT"])
def updateUsers(request, pk:int):
    User = get_user_model()
    user = User.objects.get(pk=pk)
    data = request.data
    serializer = UserSerializer(user, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response("Something went wrong")
