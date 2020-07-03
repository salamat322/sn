from django.db import models
from django.contrib.auth.models import User

from apps.posts.models import Post


class Comment(models.Model):
    comment = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='comments_like')
