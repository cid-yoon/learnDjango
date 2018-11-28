from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse

from polls.models import Question
from .models import Question, Choice


# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]

    # 최소 5개 의 투표 질문이 콤마로 분리되어 발행일에 따라 출력

    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))


def detail(request, question_id):
    return HttpResponse("You're looking at question %s" % question_id)


# 리다이렉트 된 데이터 반환
def results(request, question_id):
    question: Question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/result.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # 전송된 자료에 접근,
        selected_choice = question.choice_set.get(pk=request.POST['post'])
    except (KeyError, Choice.DoesNotExist):
        # 데이터가 없는 경우 key error, 다시 해당 화면 보여주기
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.", })
    else:  # 예외가 발생하지 않을 경우 반드시 실행, except 바로 다음에 와야 함...

        # 투표 수 증가 후 저장. 성공 시 해당 경로로 이동하여 결과 보여주기
        # 사용자가 재 전송할 url을 전달, 데이터 처리 성공시에는 항상 redirect를(웹 권장)
        selected_choice.vote += 1
        selected_choice.choice.save()

    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
