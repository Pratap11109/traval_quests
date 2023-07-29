from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class TravelGroup(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_groups')
    members = models.ManyToManyField(User, related_name='joined_groups')
    meeting_point = models.CharField(max_length=100)

    def __str__(self):
        return f"Group {self.id} - Owner: {self.owner}"


class BudgetPlanner(models.Model):
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    theme = models.CharField(max_length=100)
    num_days = models.PositiveIntegerField()
    end_date = models.DateField()
    start_date = models.DateField()

    def __str__(self):
        return f"{self.theme} - {self.end_date}"
 
