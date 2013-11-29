from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.core import serializers


from qa.models import Question, Category, Degree
from qa.forms import QuestionForm, CategoryForm, DegreeForm


def index(request):
    return HttpResponse()

@permission_required('qa.view_question')
def questions(request):
    q = request.GET.get('q')
    if q:
        questions = Question.objects.filter(question_da__icontains=q)
        if request.is_ajax():
            data = serializers.serialize("json", questions)
            return HttpResponse(data, content_type="application/json")
    else:
        questions = Question.objects.all()

    return render(request, 'questions.html', { 'questions': questions })

@permission_required('qa.add_question')
def question_add(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            # TODO use django message service
            if '_addanother' in request.POST:
                form = QuestionForm()
            else:
                return HttpResponseRedirect(reverse('questions'))
    else:
        form = QuestionForm()

    return render(request, 'question_form.html', { 'form': form,
                                                   'action': 'add' })

@permission_required('qa.change_question')
def question_edit(request, question_uuid):
    q = None
    if question_uuid:
        q = get_object_or_404(Question, uuid=question_uuid)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=q)
        if form.is_valid():
            form.save()
            # TODO use django message service
            if '_addanother' in request.POST:
                return HttpResponseRedirect(reverse('question_add'))
            else:
                return HttpResponseRedirect(reverse('questions'))
    else:
        form = QuestionForm(instance=q)

    return render(request, 'question_form.html', { 'form': form,
                                                   'action': 'edit' })

@permission_required('qa.delete_question')
def question_delete(request, question_uuid):
    q = None
    if question_uuid:
        q = Question.objects.get(uuid=question_uuid)
    if request.method == 'POST':
        if request.POST.get("post") == "yes":
            q.delete()
            return HttpResponseRedirect(reverse('questions'))
    context = { 'type': { 'name': _('question'),
                          'preview_url': 'question_edit' },
                'id': question_uuid }

    return render(request, 'delete.html', context)


@permission_required('qa.view_category')
def categories(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', { 'categories': categories })

@permission_required('qa.add_category')
def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            # TODO use django message service
            # TODO handle redirects in popup mode
            if '_addanother' in request.POST:
                form = CategoryForm()
            else:
                return HttpResponseRedirect(reverse('categories'))
    else:
        form = CategoryForm()

    return render(request, 'category_form.html', { 'form': form,
                                                   'action': 'add' })

@permission_required('qa.change_category')
def category_edit(request, category_id):
    c = None
    if category_id:
        c = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=c)
        if form.is_valid():
            form.save()
            # TODO use django message service
            # TODO handle redirects in popup mode
            if '_addanother' in request.POST:
                return HttpResponseRedirect(reverse('category_add'))
            else:
                return HttpResponseRedirect(reverse('categories'))
    else:
        form = CategoryForm(instance=c)

    return render(request, 'category_form.html', { 'form': form,
                                                   'action': 'edit' })

@permission_required('qa.delete_category')
def category_delete(request, category_id):
    c = None
    if category_id:
        c = Category.objects.get(pk=category_id)
    if request.method == 'POST':
        if request.POST.get("post") == "yes":
            c.delete()
            return HttpResponseRedirect(reverse('categories'))
    context = { 'type': { 'name': _('category'),
                          'preview_url': 'category_edit' },
                'id': category_id }

    return render(request, 'delete.html', context)


@permission_required('qa.view_degree')
def degrees(request):
    degrees = Degree.objects.all()
    return render(request, 'degrees.html', { 'degrees': degrees })

@permission_required('qa.add_degree')
def degree_add(request):
    if request.method == 'POST':
        form = DegreeForm(request.POST)
        if form.is_valid():
            form.save()
            # TODO use django message service
            # TODO handle redirects in popup mode
            if '_addanother' in request.POST:
                form = DegreeForm()
            else:
                return HttpResponseRedirect(reverse('degrees'))
    else:
        form = DegreeForm()

    return render(request, 'degree_form.html', { 'form': form,
                                                 'action': 'add' })

@permission_required('qa.change_degree')
def degree_edit(request, degree_id):
    d = None
    if degree_id:
        d = get_object_or_404(Degree, pk=degree_id)
    if request.method == 'POST':
        form = DegreeForm(request.POST, instance=d)
        if form.is_valid():
            form.save()
            # TODO use django message service
            # TODO handle redirects in popup mode
            if '_addanother' in request.POST:
                return HttpResponseRedirect(reverse('degree_add'))
            else:
                return HttpResponseRedirect(reverse('degrees'))
    else:
        form = DegreeForm(instance=d)

    return render(request, 'degree_form.html', { 'form': form,
                                                 'action': 'edit' })
    pass

@permission_required('qa.delete_degree')
def degree_delete(request, degree_id):
    d = None
    if degree_id:
        d = Degree.objects.get(pk=degree_id)
    if request.method == 'POST':
        if request.POST.get("post") == "yes":
            d.delete()
            return HttpResponseRedirect(reverse('degrees'))
    context = { 'type': { 'name': _('degree'),
                          'preview_url': 'degree_edit' },
                'id': degree_id }

    return render(request, 'delete.html', context)

# API

def search(request, apikey=None):
    pass

def rate(request, apikey=None):
    pass
