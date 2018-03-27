from django.db import models
from django.utils import timezone


class User(models.Model):
    pass


class Post(models.Model):
    title = models.CharField(max_length=15)
    text = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
