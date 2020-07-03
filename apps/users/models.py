from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Profile(models.Model):
    description = models.CharField(max_length=200)
    avatar = models.ImageField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.user.email}'s page"

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.pk})


