from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse


from forum.models import Question, Answer
from forum.forms import QuestionForm, AnswerForm

def home(request):
    questions = Question.objects.filter(published='P').order_by('-upload_time')
    for q in questions:
        q.answer_count = q.answer_set.all().count()
    return render_to_response('index.html', {'questions':questions}, context_instance=RequestContext(request))


@login_required
def ask(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.published = 'P'
            question.user = request.user
            question.save()
            return HttpResponseRedirect('/')
    else:
        question_form = QuestionForm()
    return render(request, 'forum/ask.html', {'question_form': question_form,})


@login_required
def edit_question(request, question_id):
    try:
        q = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        question_form = QuestionForm(request.POST, instance=q)
        if question_form.is_valid():
            question_form.save()
            return HttpResponseRedirect(reverse('question_page', kwargs={"question_id": q.id}))
    else:
        question_form = QuestionForm(instance=q)
    return render(request, 'forum/ask.html', {'question_form': question_form,})


@login_required
def edit_answer(request, answer_id):
    try:
        a = Answer.objects.get(id=answer_id)
    except Answer.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        answer_form = AnswerForm(request.POST, instance=a)
        if answer_form.is_valid():
            answer_form.save()
            return HttpResponseRedirect(reverse('question_page', kwargs={"question_id": a.question.id}))
    else:
        answer_form = AnswerForm(instance=a)
    return render(request, 'forum/edit_answer.html', {'answer_form': answer_form,})


def question_page(request, question_id):
    try:
        q  = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        raise Http404
    q.answer_count = q.answer_set.all().count()
    answers = Answer.objects.filter(question=q)
    answer_form = None
    user = request.user
    if user.is_authenticated():
        if request.method == 'POST':
            answer_form = AnswerForm(request.POST)
            if answer_form.is_valid():
                answer = answer_form.save(commit=False)
                answer.published = 'P'
                answer.question = q
                answer.user = request.user
                answer.save()
        else:
            answer_form = AnswerForm()
    return render(request, 'forum/question.html', {'question': q, 'answers': answers, 'answer_form': answer_form})

