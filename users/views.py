import logging
import secrets
import string

from django.utils.crypto import get_random_string
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .permissions import IsCurrentUser
from .serializers \
    import UserSerializerForOthers, \
    UserRegisterCodeAcceptSerializer, UserInviteCodeSerializer, UserEditSerializer, UserSerializer

logger = logging.getLogger(__name__)




class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if self.request.user.pk == self.kwargs.get("pk"):
            user = self.get_object()
            invite_code = user.invite_code

            invited_users = CustomUser.objects.filter(activated_invite_code=invite_code)
            invited_users_list = list(invited_users.values_list('phone', flat=True))

            return Response({'phone': user.phone,
                             'invite_code': user.invite_code,
                             'invited_users': invited_users_list})
        else:
            serializer = UserSerializerForOthers(self.get_object(),
                                                 context={'request': request})
            return Response(serializer.data)


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserEditSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsCurrentUser]

    def update(self, request, *args, **kwargs):
        password = request.data['password']
        user = request.user
        user.set_password(password)
        user.save()
        RefreshToken.for_user(user)
        return Response({'message': 'Password changed successfully'},
                        status=status.HTTP_200_OK)


class UserDeleteAPIView(generics.DestroyAPIView):
    serializer_class = UserEditSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsCurrentUser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": f"Пользователь {instance.phone} удален"}, status=status.HTTP_204_NO_CONTENT)

