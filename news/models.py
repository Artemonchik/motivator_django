from django.db import models
from django.utils import timezone


class User(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    follow_him = models.ManyToManyField('self', symmetrical=False, related_name='follow_he')
    stars = models.IntegerField()
    completed_tasks = models.IntegerField()
    # Foreing Key from Posts

    def __str__(self):
        return self.name + ' ' + self.surname


class Post(models.Model):
    title = models.CharField(max_length=15)
    text = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
