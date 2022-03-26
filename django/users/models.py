from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import Group
from django.db import models

class EmailAuthUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("EmailAuthUser must have an email address.")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class EmailAuthUser(AbstractBaseUser, PermissionsMixin):
    """Model for users to authenticate with email"""
    first_name   = models.CharField(max_length=60)
    last_name    = models.CharField(max_length=60)
    date_joined  = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login   = models.DateTimeField(verbose_name='last login', auto_now=True)
    email        = models.EmailField(max_length=255, unique=True)
    groups       = models.ManyToManyField(Group)
    is_admin     = models.BooleanField(default=False)
    is_active    = models.BooleanField(default=True)
    is_staff     = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = EmailAuthUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return (
            f"Email:      {self.email}\n"
            f"First name: {self.first_name}\n"
            f"Last name:  {self.last_name}"
        )

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label: str) -> bool:
        return super().has_module_perms(app_label)