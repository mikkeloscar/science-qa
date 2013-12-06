from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.core import serializers
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt


from django.db import IntegrityError
from django.db.models import Q

from urlparse import urlparse
import json


from qa.models import Question, Category, Degree, Rating
from qa.forms import QuestionForm, CategoryForm, DegreeForm
from api_key_manager.models import APIKey


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

    paginator = Paginator(questions, 20)

    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)

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
def question_edit(request, question_id):
    q = None
    if question_id:
        q = get_object_or_404(Question, pk=question_id)
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
def question_delete(request, question_id):
    q = None
    if question_id:
        q = Question.objects.get(pk=question_id)
    if request.method == 'POST':
        if request.POST.get("post") == "yes":
            q.delete()
            return HttpResponseRedirect(reverse('questions'))
    context = { 'type': { 'name': _('question'),
                          'preview_url': 'question_edit' },
                'id': question_id }

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

# REST API

def search(request, apikey=None):
    response = {'call': 'search'}
    if valid_api_key(apikey, request):
        query = request.GET.get('q', None)
        if query:
            query = query.split()
        categories = request.GET.get('categories', None)
        if categories:
            categories = categories.split('-')
        degree = request.GET.get('degree', None)
        locale = request.GET.get('locale', 'da')
        ku_user = request.GET.get('ku_user', None)

        q = []
        c = None
        d = None

        if locale in ['da', 'en']:
            if query:
                raw_query, params = buildSearchQuery(query, limit=5)
                q = Question.objects.raw(raw_query, params)

                if ku_user:
                    v = Rating.objects.filter(ku_user=ku_user)
                    v = v.filter(question_id__in=q)

                    ratings = []
                    for vote in v:
                        ratings.append(vote.question_id)
                    response['ratings'] = ratings

        #         q = Question.objects.all()
        #         for _q in query:
        #             q = q.filter(Q(question_da__icontains=_q) |
        #                     Q(answer_da__icontains=_q))

        #         if categories:
        #             c = q.filter(categories__category_id_da__in=categories).distinct()

        #         if degree:
        #             d = q.filter(degrees__degree_id_da=degree).distinct()

        #         # q = sortedQuery(list(q) + list(c) + list(d))

        # elif locale == 'en':
        #         q = Question.objects.all()
        #         for _q in query:
        #             q = q.filter(Q(question_en__icontains=_q) |
        #                     Q(answer_en__icontains=_q))

        #         if categories:
        #             c = q.filter(categories__category_id_en__in=categories).distinct()

        #         if degree:
        #             d = q.filter(degrees__degree_id_en=degree).distinct()
        else:
            response['error'] = 'Invalid locale'

        results = []
        for qa in q:
            results.append(qa.localeDict(locale))

        response['results'] = results
    else:
        response['error'] = 'Invalid API Key'
    return HttpResponse(json.dumps(response), content_type="application/json")

def buildSearchQuery(search, limit=None):
    # TODO limit to degree if defined
    raw = "SELECT *, "
    in_raw = []
    search_double = []
    for term in search:
        search_double.append("%" + term + "%")
        search_double.append("%" + term + "%")
        search_double.append("%" + term + "%")
        search_double.append("%" + term + "%")
        q = "CASE WHEN question_da LIKE %s THEN 1 ELSE 0 END\n"
        q += "+ CASE WHEN answer_da LIKE %s THEN 1 ELSE 0 END\n"
        q += "+ CASE WHEN question_en LIKE %s THEN 1 ELSE 0 END\n"
        q += "+ CASE WHEN answer_en LIKE %s THEN 1 ELSE 0 END"
        in_raw.append(q)
    raw += '\n+ '.join(in_raw) + ' matches\n'
    raw += "FROM qa_question HAVING matches > 0 ORDER BY matches DESC"
    if limit:
        raw += " LIMIT %d" % limit

    return (raw, search_double)


def list_qa(request, apikey=None):
    response = { 'call': 'list' }
    if valid_api_key(apikey, request):
        categories = request.GET.get('categories', None)
        if categories:
            categories = categories.split('-')
        degree = request.GET.get('degree', None)
        locale = request.GET.get('locale', 'da')
        ku_user = request.GET.get('ku_user', None)

        q = []
        c = None
        d = None

        if locale == 'da':
            if categories or degree:
                q = Question.objects.all()
                if categories:
                    q = q.filter(categories__category_id_da__in=categories).distinct()

                if degree:
                    q = q.filter(degrees__degree_id_da=degree).distinct()
        elif locale == 'en':
            if categories or degree:
                q = Question.objects.all()
                if categories:
                    q = q.filter(categories__category_id_en__in=categories).distinct()

                if degree:
                    q = q.filter(degrees__degree_id_en=degree).distinct()
        else:
            response['error'] = 'Invalid locale'

        results = []
        for qa in q:
            results.append(qa.localeDict(locale))

        response['results'] = results
    else:
        response['error'] = 'Invalid API Key'
    return HttpResponse(json.dumps(response), content_type='application/json')


def single(request, apikey=None):
    response = { 'call': 'single' }
    if valid_api_key(apikey, request):
        id = request.GET.get('id', None)
        locale = request.GET.get('locale', 'da')
        if id:
            try:
                q = Question.objects.get(pk=id)
            except ObjectDoesNotExist:
                q = None

            if q:
                q = q.localeDict(locale)
            response['question'] = q
        else:
            response['error'] = 'ID not defined'
    else:
        response['error'] = 'Invalid API Key'
    return HttpResponse(json.dumps(response), content_type='application/json')



@csrf_exempt
def rate(request, apikey=None):
    if request.method == 'POST':
        response = { 'call': 'rate' }
        # apikey = request.POST.get('apikey', None)
        if valid_api_key(apikey, request):
            id = request.POST.get('id', None)
            ku_username = request.POST.get('ku_user', "none")
            rating = int(request.POST.get('rating', 0))

            if id:
                rating = Rating(question_id=id, ku_user=ku_username, rating=rating)
                try:
                    rating.save()
                    response['success'] = True
                except (ValidationError, IntegrityError), e:
                    response['error'] = e.message

        else:
            response['error'] = 'Invalid API Key'

        if 'error' in response:
            response['succcess'] = False
        return HttpResponse(json.dumps(response), content_type='application/json')
    else:
        return HttpResponseNotAllowed(['POST'])

def valid_api_key(apikey, request):
    """ Checks if an API key is valid.
    The API Key is provided by the cleint in a HTTP request, and is looked up
    in the db to check if HTTP_REFERER and API Key domain matches.

    This check will always return True when in DEBUG mode

    """
    if settings.DEBUG:
        return True
    else:
        referer = request.META.get('HTTP_REFERER', None)
        if apikey and referer:
            uri = urlparse(referer)
            key = APIKey.objects.get(key=apikey)
            if key and key.domain == uri.netloc:
                return True
        else:
            return False

# def sortedQuery(list):
#     for arg in args:
