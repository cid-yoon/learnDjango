from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from blog.forms import PostForm
from .models import Post


# Create your views here.
def post_list(request):
    newPosts = Post.objects.filter(created_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': newPosts})


def post_detail(request, pk):
    detailPost = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': detailPost})


def post_new(request):
    form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
