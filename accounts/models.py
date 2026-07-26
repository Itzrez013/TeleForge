from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self,email,full_name,password):
        if not email:
            raise ValueError("email is empty")
        if not password:
            raise ValueError("password is empty")

        user = self.model(email=self.normalize_email(email),full_name=full_name)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,email,full_name,password):
        user = self.create_user(email,full_name,password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=60,default='کاربر جدید')
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name',]
    objects = UserManager()


    def __str__(self):
        return f"{self.full_name} - {self.email}"


class OTP(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='user_otp')
    code = models.PositiveIntegerField(validators=[MinValueValidator(100000),MaxValueValidator(999999),])
    sent_at = models.DateTimeField(auto_now=True)