from django.urls import path


from . import views

# 어플리케이션의 이름 공간 나누기
app_name = 'polls'
urlpatterns = [
    # /polls/
    path('', views.index, name='index'),

    # /polls/{num}
    path('<int:question_id>/', views.detail, name='detail'),

    # /polls/{num}/results
    path('<int:question_id>/results/', views.results, name='results'),

    # /polls/{num}/vote
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
