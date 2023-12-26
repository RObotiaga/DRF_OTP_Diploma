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


class UserCreateAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        if not phone:
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)

        otp_code = get_random_string(length=4, allowed_chars='1234567890')
        user = CustomUser(phone=phone, one_time_password=otp_code)
        user.invite_code = generate_unique_invite_code()
        user.is_active = False
        user.save()

        return Response({'message': 'OTP code sent successfully'}, status=status.HTTP_200_OK)


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

def generate_unique_invite_code():
    while True:
        invite_code = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(6))
        if not CustomUser.objects.filter(invite_code=invite_code).exists():
            return invite_code


class UserCodeAccept(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterCodeAcceptSerializer

    def create(self, request, *args, **kwargs):
        code = request.data.get('one_time_password')
        user = CustomUser.objects.get(phone=request.data.get('phone'))
        if not user.is_active:
            if code == user.one_time_password:
                password = CustomUser.objects.make_random_password()
                user.set_password(password)
                user.is_active = True
                user.save()
                return Response(
                    {'password': password},
                    status=status.HTTP_200_OK)
            return Response({'error': 'Неправильный пароль'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Аккаунт уже активирован'},
                        status=status.HTTP_400_BAD_REQUEST)


class UserInviteCode(generics.UpdateAPIView):
    serializer_class = UserInviteCodeSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = request.user  # Получение текущего авторизованного пользователя
        invite_code = request.data.get('activated_invite_code')
        print(invite_code)
        if user.activated_invite_code:
            return Response({'message': f"Invite code already activated: "
                                        f"{user.activated_invite_code}"},
                            status=status.HTTP_400_BAD_REQUEST)
        # Обновление информации о пользователе
        user.activated_invite_code = invite_code
        user.save()
        return Response({'message': f"Invite code activated successfully "
                                    f"{invite_code}"},
                        status=status.HTTP_200_OK)
