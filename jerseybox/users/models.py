from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager




class UserProfileManager(BaseUserManager):
    def create_user(self,email,username,mobile,password=None,**extra_fields):
        if not email:
            raise ValueError(("The Email must be set"))
        email=self.normalize_email(email)
        user=self.model(email=email,username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user



class UserProfile(AbstractBaseUser):
    
    
    email=models.EmailField(max_length=255)
    username=models.CharField(max_length=20)
    mobile=models.IntegerField
    password = models.CharField(("password"), max_length=128)



    objects=UserProfileManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']
