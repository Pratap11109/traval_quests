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

class Review(models.Model):
    name_of_place = models.CharField(max_length=100)
    date_of_visit = models.DateField()
    rating = models.PositiveIntegerField()
    # Choices for "What did you like most about the place?"
    LIKED_CHOICES = [
        ('Beautiful Scenery', 'Beautiful Scenery'),
        ('Good Value for Money', 'Good Value for Money'),
        ('Peaceful Environment', 'Peaceful Environment'),
        ('Cozy Ambiance', 'Cozy Ambiance'),
        ('Delicious Food', 'Delicious Food'),
        ('Clean and Well-Maintained', 'Clean and Well-Maintained'),
    ]
    liked_most = models.CharField(max_length=100, choices=LIKED_CHOICES)
    
    # Choices for "What did you not like about the place?"
    DISLIKED_CHOICES = [
        ('Noisy Environment', 'Noisy Environment'),
        ('Overpriced', 'Overpriced'),
        ('Bad Location', 'Bad Location'),
        ('Poor Food Quality', 'Poor Food Quality'),
    ]
    disliked_most = models.CharField(max_length=100, choices=DISLIKED_CHOICES)
    
    # Choices for "Overall Experience"
    EXPERIENCE_CHOICES = [
        ('Excellent', 'Excellent'),
        ('Good', 'Good'),
        ('Average', 'Average'),
        ('Poor', 'Poor'),
    ]
    overall_experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES)

    def __str__(self):
        return f"{self.name_of_place}'s Review"
    