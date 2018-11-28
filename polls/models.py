# 질문과 발행일 - 유효기간
from django.utils import timezone
import datetime
from django.db import models


# 데이터베이스 ORM, models.Model 상속
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.question_text


# 선택지와 표, 각각의 choice가 하나의 question에 관계된다는 것을 알림
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
