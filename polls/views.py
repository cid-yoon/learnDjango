import django.http
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Question, Choice


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions.
        모든 값을 가져오는 것이 아니라 게시일이 작거나 같은 Question을 포함하게 변경
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """보여줄 시간이 되지 않은 항목 감추기"""
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # 전송된 자료에 접근,
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # 데이터가 없는 경우 key error, 다시 해당 화면 보여주기
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.", })
    else:  # 예외가 발생하지 않을 경우 반드시 실행, except 바로 다음에 와야 함...

        # 투표 수 증가 후 저장. 성공 시 해당 경로로 이동하여 결과 보여주기
        # 사용자가 재 전송할 url을 전달, 데이터 처리 성공시에는 항상 redirect를(웹 권장)
        selected_choice.votes += 1
        selected_choice.save()

    return django.http.HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
