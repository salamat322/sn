from django.db import models
from django.urls import reverse

from apps.posts.models import Post


class Tag(models.Model):
    name = models.CharField(max_length=30)
    posts = models.ManyToManyField(Post, related_name='tags', blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return  reverse('tag-detail', kwargs={'pk': self.pk})

