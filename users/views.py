import logging
from twilio.rest import Client
from django.utils.crypto import get_random_string
from rest_framework import generics, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from decouple import config
from .models import CustomUser
from .permissions import IsCurrentUser
from .serializers \
    import UserSerializerForOthers, \
    UserRegisterCodeAcceptSerializer, UserInviteCodeSerializer, \
    UserEditSerializer, UserSerializer
from .services import generate_unique_invite_code

logger = logging.getLogger(__name__)

account_sid = config('TWILIO_SID')
auth_token = config('TWILIO_TOKEN')
client = Client(account_sid, auth_token)


class UserCreateAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        phone = self.request.data.get('phone')

        if not phone:
            raise serializers.ValidationError(
                {'phone': 'Phone number is required'})
        elif '+' in phone:
            raise serializers.ValidationError(
                {'phone': 'Phone number format: "7XXXXXXXXXX"'})

        otp_code = get_random_string(length=4, allowed_chars='1234567890')
        client.messages.create(
            body=otp_code,
            from_=config('NUMBER'),
            to=f'+{phone}'
        )

        user = serializer.save(one_time_password=otp_code, is_active=False)
        user.invite_code = generate_unique_invite_code()
        user.save()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if self.request.user.pk == self.kwargs.get("pk"):
            user = self.get_object()
            invite_code = user.invite_code

            invited_users = (CustomUser.objects.filter(
                activated_invite_code=invite_code)
                             .values_list('phone', flat=True))
            invited_users_list = list(invited_users)

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

    def perform_update(self, serializer):
        password = self.request.data['password']
        user = self.request.user
        user.set_password(password)
        user.save()
        RefreshToken.for_user(user)


class UserDeleteAPIView(generics.DestroyAPIView):
    serializer_class = UserEditSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsCurrentUser]


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

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        user = self.request.user
        invite_code = serializer.validated_data.get('activated_invite_code')
        if user.activated_invite_code:
            raise serializers.ValidationError(
                f"Invite code already activated: {user.activated_invite_code}"
            )
        user.activated_invite_code = invite_code
        user.save()
