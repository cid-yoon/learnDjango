from django.db import models


# 데이터베이스 ORM, models.Model 상속


# 질문과 발행일 - 유효기간
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


# 선택지와 표, 각각의 choice가 하나의 question에 관계된다는 것을 알림
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
