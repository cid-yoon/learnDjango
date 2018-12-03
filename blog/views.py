from django.shortcuts import render, get_object_or_404, redirect
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
    # post 메시지 검사, form이 유효한지 체크 후 저장
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            # 넘겨진 데이터를 바로 저장하지 않게 하는 것, 작성자 데이터 추가가 필요하니.
            # 대부분의 경우에는 True,
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form': form})


# url로부터 매개 변수 받음
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":

        # form 데이터를
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            # 넘겨진 데이터를 바로 저장하지 않게 하는 것, 작성자 데이터 추가가 필요하니.
            # 대부분의 경우에는 True,
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form': form})


def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog:post_detail', pk)
