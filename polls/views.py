from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question
from django.template import loader
from django.shortcuts import render
from django.http import Http404
from django.urls import reverse
# Create your views here.

def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	context = {
		'latest_question_list': latest_question_list,
		}
	return render(request, 'polls/index.html', context)

def detail(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
	response = "You're looking at question %s."
	return HttpResponse(response % question_id)

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
		# 템플릿에서 넘겨받은 값을 조회 request.POST['이름 or name']
	except (KeyError, ChoiceDoesNotExist):
		return render(request, 'polls/detail.html', {
			'question' : question,
			'error_message' : "You didn't select a choice.",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
	return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
