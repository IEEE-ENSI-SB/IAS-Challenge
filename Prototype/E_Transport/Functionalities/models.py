from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin, UserManager
from django.core.validators import RegexValidator
from django.utils import timezone
from django.contrib.gis.db import models


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail address")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin):
    image = models.ImageField(default='../static/images/default_image.jpg', upload_to='../static/images/', blank=True, null=False)
    email = models.EmailField(unique=True, blank=False, null=True)
    username = models.CharField(max_length=150, blank=False, null=True)
    name = models.CharField(max_length=150, blank=False, null=True)
    role = models.CharField(
        max_length=20,
        default='USER',
        blank=False,
        null=False) 
    phone = models.CharField(max_length=8, validators=[RegexValidator(r'^\d{8}$', message='Phone number must be 8 digits.')])
    position = models.PointField(null=True)
    Vehicle_Type = models.CharField(max_length = 20, blank=True, null=True)
    Charger_Type = models.CharField(max_length = 20, blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name or self.email.split('@')[0]
