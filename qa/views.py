import json
import uuid
import os
import urllib
import re

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.core import serializers
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.db.models import Q
from django.utils.text import slugify

from urlparse import urlparse

from qa.filters import PageFilter
from qa.models import Question, Category, Degree, Rating
from qa.forms import QuestionForm, CategoryForm, DegreeForm
from qa.jsonp import JsonpResponse
from api_key_manager.models import APIKey
from emaillist.models import EmailReceiver

def clean_list(list):
    l = []
    for e in list:
        if e != '' and e.isdigit():
            l.append(int(e))
    return l

def clean_order_list(list):
    l = []
    for e in list:
        if e != '':
            l.append(e)
    return l

def index(request):
    return HttpResponse()

@permission_required('qa.view_question')
def questions(request):
    query = request.GET.get('q', None)
    c = request.GET.get('c', [])
    if len(c) > 0:
        c = clean_list(c.split('.'))
    d = request.GET.get('d', [])
    if len(d) > 0:
        d = clean_list(d.split('.'))
    page = request.GET.get('p', 1)
    o = request.GET.get('o', [])

    categories = []
    degrees = []

    questions = Question.objects.all()

    if query and not request.is_ajax():
        # custom search
        q = query.split()
        raw_query, params = searchQuestionSQL(q, limit=10, degrees=d, categories=c)
        questions = Question.objects.raw(raw_query, params)
    else:
        raw_query, params = searchQuestionSQL(degrees=d,
                categories=c)
        questions = Question.objects.raw(raw_query, params)
        # if len(c) > 0:
        #     questions = questions.filter(categories__in=c)
        # if len(d) > 0:
        #     questions = questions.filter(degrees__in=d)
        # if len(o) > 0:
        #     order = clean_order_list(o.split('.'))
        #     if len(order) > 0:
        #         questions = questions.order_by(*order)

        paginator = PageFilter(request.GET, list(questions), 10)

        try:
            questions = paginator.page(page)
        except PageNotAnInteger:
            questions = paginator.page(1)
        except EmptyPage:
            questions = paginator.page(paginator.num_pages)

    # check if request is ajax
    if request.is_ajax() and query:
        # custom search
        q = query.split()
        raw_query, params = searchQuestionSQL(q, limit=5, degrees=d, categories=c)
        questions = Question.objects.raw(raw_query, params)

        user = request.user
        edit_perm = user.has_perm('qa.change_question')
        delete_perm = user.has_perm('qa.delete_question')
        # TODO grap category and degree from backend UI
        data = serializers.serialize("json", questions)
        response = { 'delete': delete_perm,
                     'edit': edit_perm,
                     'questions': data }
        return HttpResponse(json.dumps(response), content_type="application/json")


    filters = { 'categories': sorted(Category.objects.all(),
                                     key=lambda x: x.name_()),
                'degrees': sorted(Degree.objects.all(),
                                  key=lambda x: x.name_()) }

    return render(request, 'questions.html', { 'questions': questions,
                                               'filters': filters,
                                               'c': c,
                                               'd': d,
                                               'q': query })


def searchQuestionSQL(search=None, limit=None, degrees=None, categories=None,
        order=None):
    raw = """SELECT `q`.`id`, `q`.`question_da`, `q`.`answer_da`,
    `q`.`question_en`, `q`.`answer_en`, `q`.`degree_all_bsc`,
    `q`.`degree_all_msc`, `q`.`date_added`, `q`.`date_last_edit`, """
    in_raw = []
    search_double = []
    if search:
        for term in search:
            search_double.append("%" + term + "%")
            search_double.append("%" + term + "%")
            search_double.append("%" + term + "%")
            search_double.append("%" + term + "%")
            q = "CASE WHEN `q`.`question_da` LIKE %s THEN 1 ELSE 0 END "
            q += "+ CASE WHEN `q`.`answer_da` LIKE %s THEN 1 ELSE 0 END "
            q += "+ CASE WHEN `q`.`question_en` LIKE %s THEN 1 ELSE 0 END "
            q += "+ CASE WHEN `q`.`answer_en` LIKE %s THEN 1 ELSE 0 END"
            in_raw.append(q)
        raw += ' + '.join(in_raw) + ' matches, '

    raw += 'IFNULL(SUM(`r`.`rating`), 0) as rating_count '
    raw += "FROM `qa_question` `q` "
    raw += "LEFT JOIN `qa_rating` `r` ON `r`.`question_id` = `q`.`id` "

    where = []

    # limit to degree if defined
    if len(degrees) > 0:
        for degree in degrees:
            search_double.append(degree)
        raw += "INNER JOIN `qa_question_degrees` ON ( `q`.`id` ="
        raw += "`qa_question_degrees`.`question_id` ) "
        raw += "INNER JOIN `qa_degree` ON ( `qa_question_degrees`.`degree_id` "
        raw += "= `qa_degree`.`id` ) "

        where_clause = "`qa_degree`.`id` IN ("
        where_clause += ','.join(['%s' for d in degrees]) + ")"
        where.append(where_clause)

    if len(categories) > 0:
        for category in categories:
            search_double.append(category)
        raw += "INNER JOIN `qa_question_categories` ON ( `q`.`id` ="
        raw += "`qa_question_categories`.`question_id` ) "
        raw += "INNER JOIN `qa_category` ON ( `qa_question_categories`.`category_id` "
        raw += "= `qa_category`.`id` ) "

        where_clause = "`qa_category`.`id` IN ("
        where_clause += ','.join(['%s' for c in categories]) + ")"
        where.append(where_clause)

    if len(where) > 0:
        raw += "WHERE " +  ' AND '.join(where)
    raw += "GROUP BY `q`.`id` "

    if search:
        raw += " HAVING matches > 0 ORDER BY matches DESC"

    if order and not search:
        raw += "ORDER BY "
        order_by = []
        for col in order:
            dir = "DESC"
            if col[0] == '-':
                dir = "ASC"
                col = col[1:]
            order_by.append(col + " " + dir)
        order_by = ', '.join(order_by)

        raw += order_by

        # ", rating_count DESC"

    # limit results if limit is defined
    if limit:
        raw += " LIMIT %d" % limit

    return (raw, search_double)


@permission_required('qa.add_question')
def question_add(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
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
    page = request.GET.get('p', 1)
    categories = sorted(Category.objects.all(), key=lambda x: x.name_())

    paginator = PageFilter(request.GET, categories, 15)

    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categories = paginator.page(paginator.num_pages)

    return render(request, 'categories.html', { 'categories': categories })

@permission_required('qa.add_category')
def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
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
    page = request.GET.get('p', 1)
    degrees = sorted(Degree.objects.all(), key=lambda x: x.name_())

    paginator = PageFilter(request.GET, degrees, 15)

    try:
        degrees = paginator.page(page)
    except PageNotAnInteger:
        degrees = paginator.page(1)
    except EmptyPage:
        degrees = paginator.page(paginator.num_pages)

    return render(request, 'degrees.html', { 'degrees': degrees })


@permission_required('qa.add_degree')
def degree_add(request):
    if request.method == 'POST':
        form = DegreeForm(request.POST)
        if form.is_valid():
            form.save()
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
                raw_query, params = searchSQL(query, limit=5, degree=degree)
                q = Question.objects.raw(raw_query, params)

                if ku_user:
                    v = Rating.objects.filter(ku_user=ku_user)
                    v = v.filter(question_id__in=q)

                    ratings = []
                    for vote in v:
                        ratings.append(vote.question_id)
                    response['ratings'] = ratings
        else:
            response['error'] = 'Invalid locale'

        results = []
        for qa in q:
            results.append(qa.localeDict(locale))

        response['results'] = results
    else:
        response['error'] = 'Invalid API Key'
    return JsonpResponse(response, request.GET.get('callback'))


def searchSQL(search, limit=None, degree=None):
    raw = """SELECT `q`.`id`, `q`.`question_da`, `q`.`answer_da`,
    `q`.`question_en`, `q`.`answer_en`, `q`.`degree_all_bsc`,
    `q`.`degree_all_msc`, `q`.`date_added`, `q`.`date_last_edit`, """
    in_raw = []
    search_double = []
    for term in search:
        search_double.append("%" + term + "%")
        search_double.append("%" + term + "%")
        search_double.append("%" + term + "%")
        search_double.append("%" + term + "%")
        q = "CASE WHEN `q`.`question_da` LIKE %s THEN 1 ELSE 0 END "
        q += "+ CASE WHEN `q`.`answer_da` LIKE %s THEN 1 ELSE 0 END "
        q += "+ CASE WHEN `q`.`question_en` LIKE %s THEN 1 ELSE 0 END "
        q += "+ CASE WHEN `q`.`answer_en` LIKE %s THEN 1 ELSE 0 END"
        in_raw.append(q)
    raw += ' + '.join(in_raw) + ' matches, '
    raw += 'IFNULL(SUM(`r`.`rating`), 0) as rating_count '
    raw += "FROM `qa_question` `q` "
    raw += "LEFT JOIN `qa_rating` `r` ON `r`.`question_id` = `q`.`id` "

    # limit to degree if defined
    if degree:
        search_double.append(degree)
        search_double.append(degree)
        raw += "INNER JOIN `qa_question_degrees` ON ( `q`.`id` ="
        raw += "`qa_question_degrees`.`question_id` ) "
        raw += "INNER JOIN `qa_degree` ON ( `qa_question_degrees`.`degree_id` "
        raw += "= `qa_degree`.`id` ) "
        raw += "WHERE ( `qa_degree`.`degree_id_da` = %s OR "
        raw += "`qa_degree`.`degree_id_en` = %s ) "
    raw += "GROUP BY `q`.`id` "
    raw += " HAVING matches > 0 ORDER BY matches DESC, rating_count DESC"

    # limit results if limit is defined
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
        limit = request.GET.get('limit', 0)

        q = []
        c = None
        d = None

        if locale == 'da':
            if categories or degree:
                q = Question.objects.all()
                if categories:
                    for cat in categories:
                        q = q.filter(categories__category_id_da=cat).distinct()

                if degree:
                    q = q.filter(degrees__degree_id_da=degree).distinct()
        elif locale == 'en':
            if categories or degree:
                q = Question.objects.all()
                if categories:
                    for cat in categories:
                        q = q.filter(categories__category_id_en=cat).distinct()

                if degree:
                    q = q.filter(degrees__degree_id_en=degree).distinct()
        else:
            response['error'] = 'Invalid locale'

        # find ratings
        if ku_user:
            v = Rating.objects.filter(ku_user=ku_user)
            v = v.filter(question_id__in=q)

            ratings = []
            for vote in v:
                ratings.append(vote.question_id)
            response['ratings'] = ratings

        if limit != 0 and limit.isdigit():
            q = q[:int(limit)]

        results = []
        for qa in q:
            results.append(qa.localeDict(locale))

        response['results'] = results
    else:
        response['error'] = 'Invalid API Key'
    return JsonpResponse(response, request.GET.get('callback'))


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
    response = { 'call': 'rate' }
    if valid_api_key(apikey, request):
        id = request.GET.get('id', None)
        ku_username = request.GET.get('ku_user', "none")
        rating = int(request.GET.get('rating', 0))

        if id:
            rating = Rating(question_id=id, ku_user=ku_username, rating=rating)
            try:
                rating.save()
                response['success'] = True
            except (ValidationError, IntegrityError) as e:
                response['error'] = str(e)

    else:
        response['error'] = 'Invalid API Key'

    if 'error' in response:
        response['succcess'] = False

    return JsonpResponse(response, request.GET.get('callback'))


@csrf_exempt
def attachments(request, apikey=None):
    if valid_api_key(apikey, request):
        if request.method == 'POST':
            uuid = request.POST.get('uuid', None)
            response = handle_attachment(request.FILES['qa_files'], uuid)
        else:
            return HttpResponseNotAllowed(['POST'])
    else:
        response['error'] = 'Invalid API Key'

    # serve IE the right (wrong) content_type
    accept_header = request.META.get('HTTP_ACCEPT', '')
    content_types = accept_header.split(', ')

    if 'application/json' not in content_types:
        content_type = 'text/plain'
    else:
        content_type = 'application/json'

    return HttpResponse(json.dumps(response), content_type=content_type)


@csrf_exempt
def send_email(request, apikey=None):
    if valid_api_key(apikey, request):
        response = {'call': 'send_email'}

        email = None
        subject = None
        message = None
        uuid = None
        receiver = None
        files = []
        other = []

        # unpack GET data
        for key, value in request.GET.iteritems():
            if key == "qa_email":
                email = value
            elif key == "qa_subject":
                subject = value
            elif key == "qa_message":
                message = value
            elif key == "qa_receiver":
                receiver = value
            elif key == "uuid":
                uuid = value
            elif key == "locale":
                pass
            elif re.search(r'files_(\d+)', key):
                files.append(value)
            else:
                if value != "":
                    other.append((key, value))

        try:
            receiver = EmailReceiver.objects.get(receiver_id=receiver)
        except ObjectDoesNotExist:
            receiver = None

        errors = []

        request.LANGUAGE_CODE = request.POST.get('locale', 'da')

        if not email_is_valid(email):
            errors.append({'qa_email': _('Invalid mail')})
        if not subject:
            errors.append({'qa_subject': _('Empty subject')})
        if not message:
            errors.append({'qa_message': _('Empty message')})
        if not receiver:
            errors.append({'qa_receiver': _('Invalid receiver')})

        print(errors)

        if len(errors) == 0:
            # produce email and send it
            files = [generate_attachment_name(name,uuid) for name in files]
            other_fields = ["%s:%s\n" % (key, val) for key, val in other]
            email = """Form: %s
                    To: %s
                    Subject: %s

                    Files: %s

                    Other fields: %s

                    %s
                    """ % (email, receiver.email, subject, files, other_fields, message)
            print(email)
        else:
            response['errors'] = errors

    return JsonpResponse(response, request.GET.get('callback'))


def delete_attachment(request, apikey=None):
    response = {'call': 'delete_attachment'}
    if valid_api_key(apikey, request):
        uuid = request.GET.get('uuid', None)
        name = request.GET.get('name', None)
        success, msg = handle_delete_attachment(name, uuid)
        response['success'] = success
        response['name'] = name
        if not success:
            response['error'] = msg
    else:
        response['success'] = False
        response['error'] = 'Invalid API Key'
    return JsonpResponse(response, request.GET.get('callback'))


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

# TODO refactor to other file since this is not view related
def handle_attachment(f, uuid):
    """
    save attachment and return dict with file info
    """
    filename = generate_attachment_name(f.name, uuid)
    if filename:
        pathname = os.path.join(settings.ATTACHMENT_ROOT, filename)
        with open(pathname, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        response = { 'files': [ { 'name': f.name,
                          'uuid': uuid,
                          'size': f.size,
                          'content_type': f.content_type } ] }
    else:
        response['error'] = 'Invalid uuid'

    return response

def generate_attachment_name(name, uuid):
    """
    Generate filename based on uuid and filename
    """
    filename = None
    if uuid and name:
        match = re.search(r'[a-f\d]{8}-([a-f\d]{4}-){3}[a-f\d]{12}', uuid)
        if match:
            name = [slugify(p) for p in name.split('.')]
            name = '.'.join(name)
            filename = uuid + '_' + name
    return filename

def handle_delete_attachment(name, uuid):
    """
    Delete attachment from server
    """
    filename = generate_attachment_name(name, uuid)
    success = False
    msg = ""
    if filename:
        pathname = os.path.join(settings.ATTACHMENT_ROOT, filename)
        if os.path.exists(pathname):
            try:
                os.remove(pathname)
                success = True
            except OSError as e:
                msg = str(e)
        else:
            msg = "File does not exist"
    else:
        msg = "Invaid filename"
    return (success, msg)

def email_is_valid(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False
