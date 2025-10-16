from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def _create_user_obj(self, username, password, **kwargs):
        if not username:
            raise ValueError("Can not create a user without a username")

        if not password:
            raise ValueError("Can not create a user without a password")

        user = self.model(username=username, **kwargs)  # create new user object
        user.set_password(password)  # hash password
        return user

    def create_user(self, username, password, **kwargs):
        user = self._create_user_obj(username, password, **kwargs)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self._create_user_obj(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
