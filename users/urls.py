from django.urls import path
from .views import UserUpdateAPIView, UserRetrieveAPIView, \
    UserCreateAPIView, UserCodeAccept, UserInviteCode, UserDeleteAPIView
from .apps import UsersConfig
from rest_framework_simplejwt.views \
    import TokenRefreshView, TokenObtainPairView

app_name = UsersConfig.name

urlpatterns = [
    path('edit/<int:pk>/', UserUpdateAPIView.as_view(),
         name='edit-user'),
    path('user/<int:pk>/', UserRetrieveAPIView.as_view(),
         name='view-user'),
    path('register/', UserCreateAPIView.as_view(),
         name='create-user'),
    path('delete/<int:pk>/', UserDeleteAPIView.as_view(),
         name='delete-user'),
    path('code/', UserCodeAccept.as_view(),
         name='code-accept'),
    path('invite/', UserInviteCode.as_view(),
         name='invite-code'),
    path('token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
]
