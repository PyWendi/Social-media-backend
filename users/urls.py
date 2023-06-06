from django.urls import path
from . import views
from .views import (
    MyTokenObtainPairView,
    UserRegisterView,
)

# Token view
from rest_framework_simplejwt.views import (
    # TokenObtainPairView,
    TokenVerifyView,
    TokenRefreshView,
)


urlpatterns = [
    path("getRoutes", views.getRoutes, name="getRoutes"),

    # TOKEN VIEWS SECTION
    # Register and login url
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("register/", UserRegisterView.as_view(), name="Register-view"),
    
    
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    
    path("token/lifetime/", views.getLifetime, name="get-token-lifetime"),
    
    path("page_followed/", views.pageFollowed),
    path("getUsers/", views.getUsers, name="get_user"),
    path("updateUsers/<int:pk>/", views.updateUsers, name="update_user"),
    path("getUser/<int:pk>", views.getUser, name="get_single_user"),
]
