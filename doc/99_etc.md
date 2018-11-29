# 생각나는데로



### 장고 서비스 버전

* 2.x로 옮기는 것 고려
  * https://docs.djangoproject.com/en/2.1/releases/2.0/

```txt
django 2.0 supports Python 3.4, 3.5, 3.6, and 3.7. We **highly recommend** and only officially support the latest release of each series.

The Django 1.11.x series is the last to support Python 2.7.

Django 2.0 will be the last release series to support Python 3.4. If you plan a deployment of Python 3.4 beyond the end-of-life for Django 2.0 (April 2019), stick with Django 1.11 LTS (supported until April 2020) instead. Note, however, that the end-of-life for Python 3.4 is March 2019.


Third-party library support for older version of Django

Following the release of Django 2.0, we suggest that third-party app authors drop support for all versions of Django prior to 1.11. At that time, you should be able to run your package’s tests using python -Wd so that deprecation warnings do appear. After making the deprecation warning fixes, your app should be compatible with Django 2.0.
```





### 삽질

* 앱 내 urls.py 의 urlpatterns 가 list가 아닌 dict로 되어 있던 문제
  * 복사 해서 넣는 도중 바뀌어서 제대로 읽어 들이지 못한 문제로 생각 될 수도 있지만 ['set object is not reversible and argument'](https://stackoverflow.com/questions/43304923/typeerror-at-admin-set-object-is-not-reversible-and-argument-to-reverse-m) 사례로 보아 1.x버전과 2.x 버전의 템플릿 생성의 문제일 수도 있다고 생각 됨



### 서드파티

* https://django-debug-toolbar.readthedocs.io/en/latest/installation.html
  * pip install Django-debug-toolbar
* https://django-extensions.readthedocs.io/en/latest/runserver_plus.html
  * pip install Django-extensions
  * runserver_plus
    * pip install Werkzeug
    * MIDDLEWARE
      * debug_toolbar.middleware.DebugToolbarMiddleware