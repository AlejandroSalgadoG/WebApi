import uuid
import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


def recipe_image_file_path(instance, file_name):
    _, ext = os.path.splitext(file_name)
    return os.path.join("uploads", "recipe", f"{uuid.uuid4()}{ext}")


class UserManager(BaseUserManager):
    def _create_user_obj(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("user must have an email address")

        user = self.model(email=self.normalize_email(email), **kwargs)  # create new user object
        user.set_password(password)  # hash password
        return user

    # password is set to none to allow the creation of an unusable user for testing
    # this is the default behavior of the django user model
    def create_user(self, email, password=None, **kwargs):
        user = self._create_user_obj(email, password, **kwargs)
        user.save(using=self._db)  # best practice is to select database (usefull when working with multiple db)
        return user

    def create_superuser(self, email, password):
        user = self._create_user_obj(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
        


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Recipe(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # defined in settings.py
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)  # handle long text
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title
