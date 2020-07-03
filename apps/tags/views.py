from django.shortcuts import render, redirect

from .models import Tag
from .forms import TagForm


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'tags/tags_list.html', locals())


def tag_create(request):

    if request.method == 'POST':
        form = TagForm()
        if form.is_valid():
            form.save()
            return redirect(form.instance.get_absolute_url())
    else:
        form = TagForm()

    return render(request, 'tags/tag_create.html', locals())


def tag_detail(request, pk):
    tag = Tag.objects.get(pk=pk)
    return render(request, 'tags/tag_detail.html', locals())