from django.urls import path


from . import views

# 어플리케이션의 이름 공간 나누기
app_name = 'blog'
urlpatterns = [
    # /blog/
    path('', views.post_list, name='post_list'),

    # /blog/post_detail/<int:pk>
    path('post/<int:pk>/', views.post_detail, name='post_detail'),

]
