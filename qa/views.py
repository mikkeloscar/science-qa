from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse

from qa.models import Question, Category, Degree
from qa.forms import QuestionForm


def index(request):
    return HttpResponse()


@login_required
def questions(request):
    questions = Question.objects.all()
    return render(request, 'questions.html', { 'questions': questions })

@login_required
def question_add(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            # TODO use django message service
            return HttpResponseRedirect(reverse('questions'))
    else:
        form = QuestionForm()

    return render(request, 'question_form.html', { 'form': form, 
                                                   'action': 'add' })

@login_required
def question_edit(request, question_uuid):
    q = None
    if question_uuid:
        q = get_object_or_404(Question, uuid=question_uuid)
    if request.method == 'POST':
        print(q)
        form = QuestionForm(request.POST, instance=q)
        if form.is_valid():
            form.save()
            # TODO use django message service
            return HttpResponseRedirect(reverse('questions'))
    else:
        form = QuestionForm(instance=q)

    return render(request, 'question_form.html', { 'form': form,
                                                   'action': 'edit' })

@login_required
def question_delete(request, question_uuid):
    pass


@login_required
def categories(request):
    pass

@login_required
def category_add(request, category_uuid):
    pass

@login_required
def category_edit(request, category_uuid):
    pass

@login_required
def category_delete(request, category_uuid):
    pass


@login_required
def degrees(request):
    pass

@login_required
def degree_add(request, degree_uuid):
    pass

@login_required
def degree_edit(request, degree_uuid):
    pass

@login_required
def degree_delete(request, degree_uuid):
    pass


# API

def search(request):
    pass
