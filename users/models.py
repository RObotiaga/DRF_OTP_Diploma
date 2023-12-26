from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class CustomUser(AbstractUser):
    username = None

    email = models.EmailField(verbose_name='почта')
    phone = models.CharField(max_length=20,
                             verbose_name='номер',
                             unique=True)
    city = models.CharField(max_length=20,
                            verbose_name='город',
                            blank=True)
    avatar = models.ImageField(upload_to='avatar/',
                               verbose_name='аватар')
    invite_code = models.CharField(max_length=6,
                                   verbose_name='инвайт код',
                                   unique=True)
    activated_invite_code = models.CharField(max_length=6,
                                             verbose_name='активированный код',
                                             **NULLABLE)
    one_time_password = models.CharField(max_length=4,
                                         verbose_name='код подтверждения')

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
