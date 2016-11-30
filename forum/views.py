from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response
from django.template import RequestContext

from forum.models import Question, Answer
from forum.forms import QuestionForm

def home(request):
    questions = Question.objects.filter(published='P').order_by('-upload_time')
    for q in questions:
        q.answer_count = q.answer_set.all().count()
    return render_to_response('index.html', {'questions':questions}, context_instance=RequestContext(request))


@login_required
def profile(request):
    pass  # TODO


@login_required
def ask(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.published = 'P'
            question.save()
            return HttpResponseRedirect('/')
    else:
        question_form = QuestionForm()
    return render(request, 'forum/ask.html', {'question_form': question_form,})


def question_page(request, question_id):
    try:
        q  = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        raise Http404
    q.answer_count = q.answer_set.all().count()
    answers = Answer.objects.filter(question=q)
    return render(request, 'forum/question.html', {'question': q, 'answers': answers,})

