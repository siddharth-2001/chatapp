from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, name, phone,  password, email=None,):
     
        if not name:
            raise ValueError("Users must have a name")

        elif not phone:
            raise ValueError("Users must have a phone number")
        
        elif not password:
            raise ValueError("Users must have a password")
        
            
        user = self.model(
            name=name,
            phone=phone,
            email=email,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, name, email=None, password=None):
    
        user = self.create_user(
            phone=phone,
            name=name,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):

    name = models.CharField(max_length=128)
    phone = models.CharField(unique=True, max_length=20)
    email = models.EmailField(blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.name
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    
