from django.shortcuts import render, redirect

from .models import Comment
from .forms import CommentForm

from apps.posts.models import Post


def delete_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    post = comment.post
    if request.method == 'POST':
        comment.delete()
        return redirect(post.get_absolute_url())
    return redirect(request, 'posts/comment_delete.html')


