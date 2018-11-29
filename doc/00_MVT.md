# MVT ( Model View Tempalte)

* MVC와 동일 View == Controller, Template == View
* 대체 왜 이런거니..

## 흐름



```sequence
Browser->Server: Request
Server->View:Urlconf
View->Model: Model CRUD
Model->DB: ORM
DB->Model: Data
View->Template: TemplateRendering
Server->Browser: Response
```



* 클라이언트로부터 요청을 받으면 **URLconf**를 이용하여 URL 분석
* URL 분석 결과를 통해 해당 URL에 대한 처리를 담당할 **뷰** 결정
* 뷰는 자신의 로직을 실행하면서, 만일 데이터베이스 처리가 필요하면 **모델**을 통해 처리하고 그 결과를 반환
* 뷰는 자신의 로직 처리가 끝나면 템플릿을 사용하여 클라이언트에 전송할 HTML 파일을 생성
* 뷰는 최종 결과로 HTML 파일을 클라이언트에게 보내 응답





### Model - 데이터베이스

* Model
  * 사용할 데이터에 대한 정의를 담고 있는 장고의 클래스
  * ORM(Object Relation Mapper)을 사용하여 애플리케이션에서 사용할 데이터베이스를 클래스로 매핑
  * 하나의 모델 클래스는 하나의 테이블에 매핑되고, 모델 클래스의 속성은 테이블의 컬럼에 매핑
  * 추상 레이어를 통하여 API 변경 최소화
* 예시

```sql
// DDL을 통한 테이블 생성
// id라는 primary key를 가지며 first_name, last_name의 길이 제한이 30인 테이블 생성
CREATE TABLE app_user(
	"id" serial NOT NULL PRIMARY KEY,
    "first_name" varchar(30) NOT NULL,
    "last_name" varchar(30) NOT NULL
);
```



```python
## ORM 모델 정의
# 테이블 정에 맞추어 클래서 제약 사항 추가
# 테이블 명은 애플리케이션 명과 모델 클래스명을 밑줄(_)로 연결하고 모두 소문자로 표시, 다른 이름 지정도 가능
	# app_user
# Primary Key는 user 클래스에서 정의하지 않아도 장고에서 자동 부여, 원한다면 개발자가 직접 지정 가능
from django.db import models

class User(models.Model):
    # max_length=30 == varchar(30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

```



### URLconf (URL 분석)

* URL과 처리 함수를 별도로 정의, 이 둘을 매핑하는 형태
  * 정의와 기능 분리를 통해 수정이 용이하게

```python
from django.urls import path
from . import views

# 꺾쇠<> 부분의 문자열 추출을 통하여 인자 값으로 전달
# 장고에서는 path converter라고 부름
# 개발자가 추가로 타입 등록도 가능
urlpatterns = [
    
    # 일반 경로 지정에는 path
    path('users/', views.users),
    # views.find_user_for_year(reuqest, year=xxxx) 형태로 호출됨
    path('users/<int:year>/', views.find_user_for_year),
    path('users/<string:uid>/', views.find_user)
    
    # 정교하게 정의하는 경우에는 re_path
    # 정규 표현식 (0-9로 이뤄진 4자리 숫자만 매칭 )
    # 2.0부터 제공되네요..
    repath(r'^users/(?P<year>[0-9]{4})/$', views.find_user_for_year)
]
```



* URL 분석 순서
  * setting.py 파일의 ROOT_URLCONF 항목을 읽어 최상위 URL_conf(urls.py)의 위치 획득
  * URLconf를 로딩하여 urlpatterns 변수에 지정되어 있는 URL 리스트를 검사
  * 위에서 순서대로 URL 리스트의 내용을 검사하며 URL 패턴이 매칭되면 검사를 종료
  * 매치된 URL의 뷰를 호출, 여기서 뷰는 함수 또는 클래스의 메소드.
  * 호출 시 HttpReuqest 객체와 매치할 때 추출된 단어들을 뷰에 인자로 넘겨줌
  * URL 리스트 끝까지 검사했는데도 매칭에 실패하면 에러를 처리하는 뷰를 호출
* path converter
  * 타입 지정 되지 않으면 디폴트롤 str
  * slug : slug 형식의 문자열(ASCII, 숫자, 하이픈, 밑줄)과 매치
  * uuid : UUID형식 문자열과 매칭. 매치된 문자열은 파이썬의 UUID 타입으로 변환
  * Path : /(슬래시)를 포함한 모든 문자열과 매칭, 이는 URL 패턴의 일부가 아니라 전체를 추출하고자 할 때 사용
  * 정규 표현식을 사용하여서도 처리 가능 



### View - 로직 정의( Controller)

* Url 분석 이후 매핑된 뷰를 호출
  * 이벤트 핸들러
  * 웹 요청을 받아 DB 접속 등 해당 애플리케이션의 로직에 맞는 처리를 하고 결과 데이터를 HTML로 변환하는 역활
* 함수 또는 클래스의 메소드로 작성되며, 여러가지 응답을 반환
  * 응답은 HTML 또는 리다리렉트, 에러 등 여러가지 응답을 할 수 있음
  * 이런 응답 처리를 위해 로직을 뷰에 작성하는것 - views.py
    * 원한다면 다른 파일에 작성해도 무방하지만 경로에 파일이 존재해야만 찾을 수 있음

```python
# 함수로 뷰를 작성한 예시
from django.http import HttpResponse
import datetime

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s</body></html>" % now
    # 결과 처리를 위해 HttpResponse 반환
    # 일반적으로 별도의 템플릿 코드를 사용하여 처리
    return HttpResponse(html)


```



### Template - 화면 UI 정의

* 우리는 Vue.js를 통해 구성하기 때문에 동적 페이지를 쓸 일이 거의 없을 듯
* 가볍게 보고 넘어가기. Settings.py 에 정의된 경로를 통해 템플릿 참조 가능