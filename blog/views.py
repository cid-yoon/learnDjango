from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from blog.forms import PostForm, CommentForm
from .models import Post, Comment


# Create your views here.
def post_list(request):
    newPosts = Post.objects.filter(created_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': newPosts})


def post_detail(request, pk):
    detailPost = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': detailPost})


@login_required
def post_new(request):
    # post 메시지 검사, form이 유효한지 체크 후 저장
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            # 넘겨진 데이터를 바로 저장하지 않게 하는 것, 작성자 데이터 추가가 필요하니.
            # 대부분의 경우에는 True,
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form': form})


# url로부터 매개 변수 받음
@login_required
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
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog:post_detail', pk)


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blog:post_list')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog:post_detail', pk)
    else:
        form = CommentForm()

    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog:post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('blog:post_detail', pk=comment.post.pk)
