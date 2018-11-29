# 테스트

* 유닛 테스트와 클라이언트 테스트



### 유닛 테스트

* App 내부의 tests.py를 통하여 테스트



### 모델 테스트

* 모델 자체를 임의 생성하여 작업 테스트

```python
class QuestionModelTest(TestCase):
    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        # 객체 생성, 저장하지 않기에 실제 영향을 주지는 않음
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

```



### 뷰 테스트

* 라우팅을 통해 호출되는 것처럼 테스트 케이스 작성
  * 유틸리티 함수를 통해 모델 객체를 생성

```python
def create_question(question_text, days):
    """질문 생성 함수, 유틸리티, 현재 시간 이후만 생성되게~"""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)
```

* 

```python
class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """문제가 없을 경우 출력 테스트"""
        
        # reverse를 통해 url을 얻어와 , client 호출을 수행
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "no polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
        
        
    def test_future_question_and_past_question(self):
        # 임시 모델 객체를 생성하여 테스트
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            

```



