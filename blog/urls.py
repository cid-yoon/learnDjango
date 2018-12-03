from django.urls import path

from . import views

# 어플리케이션의 이름 공간 나누기
app_name = 'blog'
urlpatterns = [
    # /blog/
    path('', views.post_list, name='post_list'),

    # /blog/post_detail/<int:pk>
    path('post/<int:pk>/', views.post_detail, name='post_detail'),

    # /blog/post/new/
    path('post/new/', views.post_new, name='post_new'),

    # /blog/post/edit/
    path('post/edit/<int:pk>', views.post_edit, name='post_edit'),

    # /blog/post/drafts
    path('post/drafts/', views.post_draft_list, name='post_draft_list'),

    # /blog/<int:pk>/publish
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),

    # /blog/<int:pk>/remove
    path('post/<int:pk>/remove/', views.post_remove, name='post_remove'),

    # /blog/post/<int:pk>/comment
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),

    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),

    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),

]
