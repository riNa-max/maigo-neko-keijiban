from django.db import models
from django.contrib.auth.models import AbstractUser

class Account(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="メールアドレス")
    username = models.CharField(max_length=150, verbose_name="ユーザー名")
    phone_number = models.CharField(max_length=15, verbose_name="電話番号", blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
