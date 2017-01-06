from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response
from django.template import RequestContext


from forum.models import Question, Answer, Tag, UniversityField
from forum.forms import QuestionForm, AnswerForm


PAGE_SIZE = 2  # TODO


def home(request):
    questions = Question.objects.filter(published='P').order_by('-upload_time')
    paginator = Paginator(questions, PAGE_SIZE)
    page = request.GET.get('page')
    if not page:
        page = 1
    try:
        page = int(page)
    except ValueError:
        page = 1
    page_questions = paginator.page(page)
    for question in page_questions:
        question.answer_count = question.answer_set.all().count()  # TODO annotate
    return render_to_response('index.html', {'questions': page_questions}, context_instance=RequestContext(request))


def _get_or_create_tags(data):
    raw_tags = data.strip().split()
    tags = []
    for t in raw_tags:
        tag = Tag.objects.filter(name=t).first()
        if tag != None:
            tags.append(tag)
        else:
            new_tag = Tag.objects.create(name=t)
            tags.append(new_tag)
    return tags


@login_required
def ask(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.published = 'P'
            question.user = request.user
            question.save()
            question_form.save_m2m()
            question.tags.add(*_get_or_create_tags(question_form.cleaned_data['tags']))
            return HttpResponseRedirect('/')
    else:
        question_form = QuestionForm()
    return render(request, 'forum/ask.html', {'question_form': question_form})


@login_required
def edit_question(request, question_id):
    try:
        q = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        question_form = QuestionForm(request.POST, instance=q)
        if question_form.is_valid():
            question = question_form.save()
            question.tags.add(*_get_or_create_tags(question_form.cleaned_data['tags']))
            return HttpResponseRedirect(reverse('question_page', kwargs={"question_id": q.id}))
    else:
        question_form = QuestionForm(instance=q, initial={'tags': ' '.join(q.tags.all().values_list('name', flat=True))})
    return render(request, 'forum/ask.html', {'question_form': question_form})


@login_required
def remove_question(request, question_id):
    try:
        q = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        raise Http404
    q.published = 'R'
    q.save()
    return HttpResponseRedirect(reverse('home'))


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
    return render(request, 'forum/edit_answer.html', {'answer_form': answer_form})


@login_required
def remove_answer(request, answer_id, question_id):
    try:
        a = Answer.objects.get(id=answer_id)
    except Answer.DoesNotExist:
        raise Http404
    a.published = 'R'
    a.save()
    return HttpResponseRedirect(reverse('question_page', kwargs={"question_id": a.question.id}))


def question_page(request, question_id):
    try:
        q = Question.objects.filter(published='P').get(id=question_id)
    except Question.DoesNotExist:
        raise Http404
    answer_form = None
    user = request.user
    if user.is_authenticated():
        if request.method == 'POST':
            answer_form = AnswerForm(request.POST)
            if answer_form.is_valid():
                answer = answer_form.save(commit=False)
                answer.published = 'P'
                answer.question = q
                answer.user = user
                if user == q.user:
                    q.answer_set.all().update(accepted=False)
                    answer.accepted = True
                answer.save()
        else:
            answer_form = AnswerForm()

    q.answer_count = q.answer_set.all().count()
    answers = Answer.objects.filter(question=q, published='P').order_by('-accepted')

    if request.user != None:
        q.is_stared = q.stars.filter(id=request.user.id).exists()
        for a in answers:
            a.is_stared = a.stars.filter(id=request.user.id).exists()

    return render(request, 'forum/question.html', {'question': q, 'answers': answers, 'answer_form': answer_form})


@login_required
def star_question(request, question_id):
    try:
        q = Question.objects.filter(published='P').get(id=question_id)
    except Question.DoesNotExist:
        raise Http404
    if not q.stars.filter(id=request.user.id).exists():
        q.stars.add(request.user)
    return HttpResponseRedirect(reverse('question_page', kwargs={"question_id": q.id}))


@login_required
def unstar_question(request, question_id):
    try:
        q = Question.objects.filter(published='P').get(id=question_id)
    except Question.DoesNotExist:
        raise Http404
    if q.stars.filter(id=request.user.id).exists():
        q.stars.remove(request.user)
    return HttpResponseRedirect(reverse('question_page', kwargs={"question_id": q.id}))


@login_required
def star_answer(request, answer_id):
    try:
        a = Answer.objects.get(id=answer_id)
    except Answer.DoesNotExist:
        raise Http404
    if not a.stars.filter(id=request.user.id).exists():
        a.stars.add(request.user)
    return HttpResponseRedirect(reverse('question_page', kwargs={"question_id": a.question.id}))


@login_required
def unstar_answer(request, answer_id):
    try:
        a = Answer.objects.get(id=answer_id)
    except Answer.DoesNotExist:
        raise Http404
    if a.stars.filter(id=request.user.id).exists():
        a.stars.remove(request.user)
    return HttpResponseRedirect(reverse('question_page', kwargs={"question_id": a.question.id}))


@login_required
def accept_answer(request, answer_id):
    try:
        a = Answer.objects.get(id=answer_id)
    except Answer.DoesNotExist:
        raise Http404
    if a.question.user != request.user:
        raise Http404  # TODO replace with forbidden
    a.question.answer_set.all().update(accepted=False)
    a.accepted = True
    a.save()
    return HttpResponseRedirect(reverse('question_page', kwargs={"question_id": a.question.id}))


@login_required
def reject_answer(request, answer_id):
    try:
        a = Answer.objects.get(id=answer_id)
    except Answer.DoesNotExist:
        raise Http404
    if a.question.user != request.user:
        raise Http404  # TODO replace with forbidden
    a.accepted = False
    a.save()
    return HttpResponseRedirect(reverse('question_page', kwargs={"question_id": a.question.id}))


def search(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            questions = Question.objects.filter(published='P')
            for word in query.strip().split():
                questions = questions.filter(Q(title__icontains=word) | Q(description__icontains=word))
            questions = questions.annotate(cnt=Count('stars')).order_by('-cnt')
            paginator = Paginator(questions, PAGE_SIZE)
            page = request.GET.get('page')
            if not page:
                page = 1
            try:
                page = int(page)
            except ValueError:
                page = 1
            page_questions = paginator.page(page)
            for question in page_questions:
                question.answer_count = question.answer_set.all().count()  # TODO annotate
            return render_to_response('index.html', {'questions': page_questions, 'query': query, 'page_desc': query}, context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect('/')
    else:
        raise Http404


def tags(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    questions = tag.question_set.all().annotate(cnt=Count('stars')).order_by('-cnt')
    paginator = Paginator(questions, PAGE_SIZE)
    page = request.GET.get('page')
    if not page:
        page = 1
    try:
        page = int(page)
    except ValueError:
        page = 1
    page_questions = paginator.page(page)
    for question in page_questions:
        question.answer_count = question.answer_set.all().count()  # TODO annotate
    return render_to_response('index.html', {'questions': page_questions, 'page_desc': tag.name}, context_instance=RequestContext(request))


def fields(request, field_id):
    field = UniversityField.objects.get(id=field_id)
    questions = field.question_set.all().annotate(cnt=Count('stars')).order_by('-cnt')
    paginator = Paginator(questions, PAGE_SIZE)
    page = request.GET.get('page')
    if not page:
        page = 1
    try:
        page = int(page)
    except ValueError:
        page = 1
    page_questions = paginator.page(page)
    for question in page_questions:
        question.answer_count = question.answer_set.all().count()  # TODO annotate
    return render_to_response('index.html', {'questions': page_questions, 'page_desc': field.name}, context_instance=RequestContext(request))
