

# 프로젝트

* 프로젝트 개발 시 고려 할 사항 정리

## 기본 설정
* settings.py
    * 개발 모드 상황에서는 allow hosts가 기본으로 127.0.0.1로.
    * product에서는 ip 지정 필요합니다.
* 프로젝트에 포함되는 애플리케이션들은 모두 설정 파일에 등록
    * 모듈명만 등록해도 되지만, 애플리케이션의 설정 클래스로 등록하는 것이 더 명확



## 프로젝트 생성

```shell
django-admin startproject mysite	# 프로젝트 생성
python manage.py startapp polls		# 앱 생성
# settings.py 수정

python manage.py migrate			# 데이터베이스에 기본 테이블 생성
python manage.py runserver			# 현재까지 작업을 개발용 웹 서버로 확인
```



### 앱 생성

* 장고가 startapp polls 명령시에 자동 생성된 app.py 파일에 PollConfig 클래스를 찾들 수 있도록 모듈 경로까지 포함

```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'polls.apps.PollsConfig',   # 추가
]
```



### DB 엔진 설정

* 디폴트로 SQLite3 사용, 변경 위해서는 settings.py 수정

```python
# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```



### TimeZon 지정

* UTC -> 한국 변경하기가 보기엔 편함
* product에서는 UTC 권장
  * 오.. 한글도 됩니다. language ='ko-kr'



### 기본 테이블 생성

* 모든 웹 프로젝트 개발 시 반드시 사용자와 그룹 테이블이 필요하다는 가정하에 설계
* 어드민이 무조건 있어야 된다는 기준!!!

```shell
python manage.py migrate
```



### 구동

```shell
# 127.0.0.1 8000 구동
python manage.py runserver {opt:ip, default 127.0.0.1} {opt:port, default 8000}

# 127.0.0.1구동, 백그라운드에서 수행 &
python mange.py runserver &
```





### 관리자 사이트 로그인

* http://localhost:8000/admin/login/?next=/admin/
  * 기본 admin의 시작, manage.py를 통해 유저 생성 가능

```shell
python mange.py createsuperuser
```

