# mysite

* 장고 샘플 프로젝트
    * [설문조사 앱 만들기](https://docs.djangoproject.com/ko/2.1/intro/overview/)



### 사용자 스토리

* 사용자는 서비스를 통하여 현재 진행중인 설문조사를 볼 수 있다.
* 사용자는 설문조사 항목을 선택 하여, 조사 항목을 볼 수 있다.
* 사용자는 조사항목을 선택 할 수 있으며 복수 선택은 허용하지 않는다.
* 사용자는 투표 완료 버튼을 선택하여 선택한 조사 항목을 결정 할 수 있다.
* 사용자는 투표 완료 시, 다른 사용자들이 어떤 선택을 하였는지 설문 결과를 볼 수 있다.
* 사용자는 설문 조사 완료 화면에서 재 투표를 할 수 있다.



### 요구사항

- 최근에 실시하는 질문의 리스트를 보여주기
  - T : index.html
- 하나의 질문에 대해 투표할 수 있도록 답변 항목을 폼으로 보여주기
  - T : detail.html
- 질문에 따른 투표 결과를 보여주기
  - T : results.html



### 모델 정의

* Question table

* * 질문을 저장하는 테이블

Column | type | const | desc
:-----:|:----:|:-----:|:---:
id|integer|NotNull, PK, AutoIncrement|Primary Key
question_text|varchar(200)|NotNull|질문 문장
pub_date|datetime|NotNull|질문 생성 시간



* Choice table
  * 질문별로 선택용 답변 항목을 저장

|   Column    |     type     |           const            |      desc      |
| :---------: | :----------: | :------------------------: | :------------: |
|     id      |   integer    | NotNull, PK, AutoIncrement |  Primary Key   |
| choice_text | varchar(200) |          NotNull           | 답변 항목 문구 |
|  voites           |   integer   |          NotNull           | 투표 카운트 |
|  question       | integer             |   NotNull,  FK(question, id), index          |    Foregin Key            |





- 모든 컬럼은 not null로 정의하는 것이 추천
- PK는 자동 증가 속성이나, 분산 서버 환경 고려해 빼는것이 좋음(예제에서는 넣음)
- choice 테이블의 question의 경우 QuestTable과 Foreign Key 관계 설정. Index를 생성하도록 함
  - 질문에 없는 항목은 포함 될 수 없으며 검색 시 quest id를  통해 빠르게 검색 가능



