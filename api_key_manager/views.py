from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from api_key_manager.models import APIKey


def index(request):
    keys = APIKey.objects.all()
    return render(request, 'keys.html', { 'keys': keys })


@login_required
def questions(request):
    questions = Question.objects.all()
    return render(request, 'questions.html', { 'questions': questions })

@login_required
def key_edit(request):
    pass
