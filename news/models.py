from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/{1}'.format(instance.user.username, filename)


def post_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/{1}'.format(instance.author.user.username, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Ccылка на USER
    surname = models.CharField(max_length=20, default='', blank=True)  # Фамилия
    name = models.CharField(max_length=20, default='', blank=True)  # Имя
    follow_him = models.ManyToManyField('self', symmetrical=False, related_name='follow_he')  # Подписчики/Подписки
    stars = models.IntegerField(default=5)  # Звезды
    completed_tasks = models.IntegerField(default=0)  # Выполненные задания
    profile_img = models.ImageField(upload_to=user_directory_path, null=True, blank=False)

    def __str__(self):
        return self.name + ' ' + self.surname


class Post(models.Model):
    title = models.CharField(max_length=15)  # Заголовок
    text = models.TextField(max_length=110)  # Текст
    pub_date = models.DateTimeField(default=timezone.now)  # Дата публикации
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)  # Автор
    time = models.IntegerField(null=True, blank=False,
                               validators=[MaxValueValidator(100), MinValueValidator(1)])  # Срок
    image = models.ImageField(upload_to=post_directory_path, null=True)  # Картинка
    likes = models.IntegerField(default=0)  # Лайки

    def __str__(self):
        return self.title


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Dialog(models.Model):
    users = models.ManyToManyField(Profile)


class Message(models.Model):
    text = models.CharField(max_length=255)
    date = models.DateTimeField(default=timezone.now)
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE)
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
