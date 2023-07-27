from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserProfileManager(BaseUserManager):
    def create_user(self, email, username, mobile, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        if not mobile:
            raise ValueError("Users must have a mobile number")

        email = self.normalize_email(email)
        username = username.strip()
        mobile = mobile.strip()

        user = self.model(email=email, username=username, mobile=mobile)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, mobile, password=None):
        user = self.create_user(email, username, mobile, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    mobile = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'mobile']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username