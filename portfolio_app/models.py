from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)


# models.py

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse  # Add this import


class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    tagline = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='photos/', blank=True, null= True)
    about_me = models.TextField()
    experience = models.TextField()
    skills = models.TextField()
    education = models.TextField()
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    social_linkedin = models.URLField(blank=True)
    social_github = models.URLField(blank=True)
    social_twitter = models.URLField(blank=True)
    template = models.CharField(max_length=50, default='default')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('public_portfolio', args=[str(self.user.id)])


class Project(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name='projects', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='project_images/', blank=True)
    url = models.URLField(blank=True)



class Feedback(models.Model):
    portfolio = models.ForeignKey('Portfolio', on_delete=models.CASCADE, related_name='feedbacks')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.name} for {self.portfolio.user.username}'s portfolio"