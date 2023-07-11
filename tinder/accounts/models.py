from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.OneToOneField(
        User, related_name="account_user", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    zodiac = models.CharField(max_length=10)
    about_bad_habits = models.TextField()
    image = models.ImageField(upload_to="account_images/", null=True, blank=True)
    like = models.ManyToManyField(User)

    def __str__(self):
        return self.user.username


class Chat(models.Model):
    sender = models.ForeignKey(
        User, related_name="sender_user", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User, related_name="receiver_user", on_delete=models.CASCADE
    )
    message = models.TextField()
    message_time = models.DateTimeField(auto_now_add=True)
