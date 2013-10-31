from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Question, Category, Degree


def index(request):
    return HttpResponse()


@login_required
def questions(request):
    pass

@login_required
def question_add(request, question_uuid):
    pass

@login_required
def question_edit(request, question_uuid):
    pass

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
