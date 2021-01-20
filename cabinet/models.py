from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager


class AccountManager(BaseUserManager):
    """
    Кастомный менеджер модели, где электронная почта является уникальным идентификатором.
    для аутентификации вместо имени пользователя.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Создать и сохранить Пользоваиеля использую email и пароль.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Создать и сохранить Супер-Пользователя используя email и пароль.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='Email', unique=True)
    is_staff = models.BooleanField(verbose_name='Доступ в админ-панель', default=False)
    is_active = models.BooleanField(verbose_name='Активный', default=True)
    first_name = models.CharField(blank=True, max_length=30, verbose_name='Имя')
    last_name = models.CharField(blank=True, max_length=150, verbose_name='Фамилия')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон', unique=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AccountManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'
