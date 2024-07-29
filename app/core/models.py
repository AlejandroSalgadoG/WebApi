from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    # password is set to none to allow the creation of an unusable user for testing
    # this is the default behavior of the django user model
    def create_user(self, email, password=None, **kwargs):
        user = self.model(email=self.normalize_email(email), **kwargs)  # create new user object
        user.set_password(password)  # hash password
        user.save(using=self._db)  # best practice is to select database (usefull when working with multiple db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"