from django.contrib import admin

# Register your models here.

from .models import Question, Choice


# 풀스크린
# class ChoiceInline(admin.StackedInline):

# 표 형태
class ChoiceInline(admin.TabularInline):
    """Choice 객체는 Question 관리자 페이지에서 편집된다. 기본으로 3가지 선택 항목을 제공함."""
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """레이블 설정, 필드의 순서 변경"""
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

    # 필드 표시를 위한 값, ORM의 메소드 결과도 바로 사용 가능..
    # 오졌다..
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
