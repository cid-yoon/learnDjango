# 애플리케이션 개발



### 시작

* URLS를 통한 라우팅
  * 프로젝트 구조적으로 admin을 제외한 부분에서 항상 사용하기를 권장

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # include() 함수를 통해 다른 URLconf를 참조 가능
    # 해당 path 처리 이후에 남은 부분을 전달
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]

```





### 테이블 정의

* App 내부에 테이블 모델 정의

```python
from django.db import models

# Create your models here.

# 테이블을 하나의 클래스로 정의
# 테이블의 컬럼은 클래스의 변수(속성)으로 매핑
# django.db.models.Model 상속 후 각 클래스 변수의 타입도 장고에서 미리 정의된
# 필드 클래스 사용

# 클래스 변수명은 컬럼명 그대로 매핑
# __str__() 메소드는 객체를 문자열로 표현할 때 사용. 나중에 보게 될 Admin 사이트나
# 장고 쉘 등에서 테이블명을 보여줘야 하는데, 이때 __str__() 메소드를 정의하지 않으며
# 테이블명이 제대로 표시되지 않음. 


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

```

* python makemigrations XXX 로 모델 생성
* migrations에 생성된 파일을 통해 SQL 문 확인 가능
  * python manage.py sqlmigrate APPNAME FILE_PREFIX
* python manage.py check를 통해 migration을 생성하거나 데이터베이스를 건드리지 않고 project 문제 확인 가능





### admin 사이트에 테이블을 반영하기 위한 작업

* admin.py 수정

```python
from django.contrib import admin
from polls.models import Question, Choice
# Register your models here.

# 너무나도 깔끔하게 페이지에 등록, 수정, 삭제, 히스토리까지..
admin.site.register(Question)
admin.site.register(Choice)
```

* Migration 명령을 통해 db sync

```shell
# 디렉토리 하위에 마이그레이션 파일이 생성
# migrations/xxxx_initial.py
python mange.py makemigrations

# 해당 파일을 이용하여 마이그레이션
python manage.py migrate

## 마이그레이션 시 사용하는 SQL 문장 확인 가능
python manage.py sqlmigrate polls 0001


-- Create model Question
--
CREATE TABLE "polls_question" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "question_text" varchar(200) NOT NULL, "pub_date" datetime NOT NULL);
--
-- Add field question to choice
--
ALTER TABLE "polls_choice" RENAME TO "polls_choice__old";
CREATE TABLE "polls_choice" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "choice_text" varchar(200) NOT NULL, "votes" integer NOT NULL, "question_id"integer NOT NULL REFERENCES "polls_question" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "polls_choice" ("id", "choice_text", "votes", "question_id") SELECT "id", "choice_text", "votes", NULL FROM "polls_choice__old";
DROP TABLE "polls_choice__old";
CREATE INDEX "polls_choice_question_id_c5b4b260" ON "polls_choice" ("question_id");
COMMIT;
```





## View 및 Template  작업

### UrlConf

* URL 과 뷰는 1:1 또는 1:N으로 매핑 가능
* URLconf 처리가 urls.py를 통해 작성
* 프로젝트와 앱 간 구분하여 처리하는 것이 유지보수성을 위해 좋음
  * 네임스페이스처럼 사용 할 수 있음
* path() 메소드를 통하여 핸들러 처리
  * 필수 인자 
    * Route : URL 패턴을 표현하는 문자열. 
    * view : URL 스트링이 매칭되면 호출되는 뷰 함수, HttpRequest 객체와 URL 스트링에서 추출된 항목 전달
  * 선택 인자
    * kwargs : URL 스트링에서 추출된 항목 외에 추가적인 인자를 뷰 함수에 전달할 때 사용, dict로 인자 정의
    * Name: 각 URL 패턴별로 이름 지정, 템플릿 파일에서 많이 사용됨

```python
# mysite/urls.py

from django.contrib import admin
# include를 통해 app - polls로 url 처리 위임
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('/polls/', include('polls.urls')),
]
```

```python
# mysite/polls/urls.py

from django.urls import path

# 모든 뷰를 import하여 처리
from . import views

# 상대 경로로 설정하여 간략화
# int형의 questid를 인자로 전달, views.detail과 연결, named
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>', views.detail, name='detail'),
    path('<int:question_id>', views.results, name='results'),
    path('<int:question_id>', views.vote, name='vote'),

]
```



* ROOT_URLCONF설정에 의해 해댱 모듈을 검색, 패턴을 따라 라우팅
* `<int:question_id>` 괄호를 사용하여 URL 의 일부를 "캡처"하고, 해당 내용을 keyword 인수로서 view 함수로 전달
* , `<int:` 부분은 어느 패턴이 해당 URL 경로에 일치되어야 하는 지를 결정하는 컨버터.



### View

* View는 요청 정보가 담긴 HttpResponse객체를 반환하거나 Http404와 같은 예외를 발생 시켜야 함
* 모든 Django는 HttpResponse 객체나 혹은 예외를 원함
* template path의 경우 각 app 안에 포함 될 수 잇도록 구성
  * 이름 충돌 예방
  * mysite project의 polls app의 경우, mystic/polls/tempate/polls/index.html

```python
from django.http import HttpResponse

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)

```

* 하드 코딩 된 부분을 Template을 사용하여 분리

```python
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]

    # 최소 5개 의 투표 질문이 콤마로 분리되어 발행일에 따라 출력
    template = loader.get_template('polls/index.html')
    
    # template에서 쓰이는 변수명과 python의 객체를 연결하는 dict
    context ={
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))
```

* index.html ( template)

```html
{% if latest_question_list %} # View에 의해 전달된 context
    <ul>
        # 순회하며 quest id와 내용 표시
        {% for question in latest_question_list %}
            <li><a href="/polls/{{ question.id }}/">
                {{ question.question_text }}</a>
            </li>
        {% endfor %}
    </ul>
{% else %}	# 데이터가 없는 경우 
    <p>No Polls are available.</p>
{% endif %}
```

* 절대 경로를 제거

```html
<a href= "{% url 'detail' question.id %}">
                {{ question.question_text }}</a>
```

* app (urls.py)에서 설정한 namespace에 맞추어 설정

```html
<a href= "{% url 'polls:detail' question.id %}">
                {{ question.question_text }}</a>
```



### Generic

* DetailView
  * 특정 개체 유형에 대한 세부 정보 페이지 표시
  * ```<app name>/<model name>_detail.html_ 템플릿 사용```
    * Polls/question_detail.html
    * Results 리스트 뷰에 대해서 template_name 지정
* Listview
  * 개체 목록 표시
  * ```<app name>/<model name>_list.html```
* `DetailView`의 경우, `question` 변수가 자동으로 제공됩니다 - Django 모델 (`Question`)을 사용하기 때문에 Django는 컨텍스트 변수의 적절한 이름을 결정할 수 있습니다. 그러나 ListView의 경우 자동 생성 된 컨텍스트 변수는 `question_list` 입니다. 이것을 덮어 쓰려면 `context_object_name` 속성을 제공하고, 대신에 `latest_question_list`를 사용하도록 지정하십시오. 다른 접근 방법으로, 템플릿을 새로운 기본 컨텍스트 변수와 일치하도록 변경할 수 있습니다. 그러나 원하는 변수를 사용하도록 Django에 지시하는 것이 훨씬 쉽습니다.