from django.shortcuts import render, redirect

from .models import Post
from .forms import PostCreateForm, PostUpdateForm

from apps.tags.models import Tag
from apps.tags.forms import TagForm
from apps.comments.forms import CommentForm, Comment


def main_page(request):
    posts = Post.objects.all().order_by('-pk')
    return render(request, 'posts/main_page.html', locals())


def create_post(request):
    if request.method == 'POST':
        post_form = PostCreateForm(request.POST, request.FILES)
        tag_form = TagForm(request.POST)
        if post_form.is_valid() and tag_form.is_valid():
            user = request.user
            post_form.instance.user = user
            post_form.save()
            tag_name = tag_form.cleaned_data.get('name')
            tag = Tag.objects.get_or_create(name=tag_name)
            tag[0].posts.add(post_form.instance)
            return redirect(post_form.instance.get_absolute_url())
    else:
        post_form = PostCreateForm()
        tag_form = TagForm()
    return render(request, 'posts/post_create.html', locals())


def delete_post(request, pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect('posts-page')
    return render(request, 'posts/post_delete.html')


def update_post(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        form = PostUpdateForm(request.POST or None, request.FILES or None, instance=post,
                              initial={'title': post.title, 'content': post.content})
        if form.is_valid():
            form.save()
        return redirect(post.get_absolute_url())
    else:
        form = PostUpdateForm()
    return render(request, 'posts/post_update.html', locals())


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.instance.user = request.user
            comment_form.instance.post = post
            comment_form.save()
        if 'like' in request.POST:
            if request.user in post.likes.all():
                post.likes.remove(request.user)
            else:
                post.likes.add(request.user)
        return redirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()
    return render(request, 'posts/post_detail.html', locals())


def delete_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    post = comment.post
    if request.method == 'POST':
        comment.delete()
        return redirect(post.get_absolute_url())
    return redirect(request, 'posts/comment_delete.html')
