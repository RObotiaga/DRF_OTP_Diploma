from rest_framework import serializers

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('phone',)


class UserSerializerForOthers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('phone', 'invite_code',)


class UserEditSerializer(serializers.ModelSerializer):
    phone = serializers.ReadOnlyField()

    class Meta:
        model = CustomUser
        fields = ('phone', 'password',)


class UserRegisterCodeAcceptSerializer(serializers.ModelSerializer):
    password = serializers.ReadOnlyField()

    class Meta:
        model = CustomUser
        fields = ('phone', 'one_time_password', 'password')


class UserInviteCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('phone', 'activated_invite_code')
