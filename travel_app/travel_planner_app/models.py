from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class TravelGroup(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_groups')
    members = models.ManyToManyField(User, related_name='joined_groups')
    meeting_point = models.CharField(max_length=100)

    def __str__(self):
        return f"Group {self.id} - Owner: {self.owner}"

# class ExternalUserManager(BaseUserManager):
            
#     def create_user(self, email, username, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         if not username:
#             raise ValueError('The Username field must be set')

#         email = self.normalize_email(email)
#         user = self.model(email=email, username=username, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, username, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')

#         return self.create_user(email, username, password, **extra_fields)

# class ExternalUser(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(max_length=255, unique=True)
#     username = models.CharField(max_length=30, unique=True)
#     is_active = models.BooleanField(default=True)

#     objects = ExternalUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']

#     def __str__(self):
#         return self.email
