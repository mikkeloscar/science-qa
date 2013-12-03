from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_noop as __

from uuidfield import UUIDField

class Question(models.Model):
    uuid = UUIDField(auto=True)
    question_da = models.CharField(_('question da'), max_length=200, blank=True)
    answer_da = models.TextField(_('answer da'), blank=True)
    question_en = models.CharField(_('question en'), max_length=200, blank=True)
    answer_en = models.TextField(_('answer en'), blank=True)
    categories = models.ManyToManyField('Category', related_name="cat+",
            verbose_name=_('Categories'))
    degrees = models.ManyToManyField('Degree', related_name="degree+",
            verbose_name=_('Degrees'))
    degree_all_bsc = models.BooleanField(_('All Bsc degrees'))
    degree_all_msc = models.BooleanField(_('All Msc degrees'))
    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_last_edit = models.DateTimeField(_('last edit'), auto_now=True)

    class Meta:
        verbose_name = _('question')
        verbose_name_plural = _('questions')
        # extend permissions created by django-admin
        permissions = (("view_question", "Can view question"),)

    def question(self, lang):
        if lang == "en":
            return self.question_en
        else:
            return self.question_da or self.question_en

    def answer(self, lang):
        if lang == "en":
            return self.answer_en
        else:
            return self.answer_da or self.answer_en

    def localeDict(self, lang):
        LANGS = ['da', 'en']
        if lang in LANGS:
            result = { 'question': self.question(lang),
                       'answer': self.answer(lang) }
            return result
        else:
            return None

    def __unicode__(self):
        return self.question_da or self.question_en


class Category(models.Model):
    name_da = models.CharField(_('Category name (da)'), max_length=200,
            blank=True)
    name_en = models.CharField(_('Category name (en)'), max_length=200,
            blank=True)
    category_id_da = models.CharField(_('Category ID (da)'), max_length=200,
        help_text=_('The category ID is used to refrence category in the url @'
                    + ' kunet.dk'), blank=True)
    category_id_en = models.CharField(_('Category ID (en)'), max_length=200,
        help_text=_('The category ID is used to refrence category in the url @'
                    + ' kunet.dk'), blank=True)
    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_last_edit = models.DateTimeField(_('last edit'), auto_now=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        # extend permissions created by django-admin
        permissions = (("view_category", "Can view category"),)

    def name(self, lang):
        if lang == "en":
            return self.name_en
        else:
            return self.name_da or self.name_en

    def __unicode__(self):
        return self.name_da or self.name_en


class Degree(models.Model):
    BACH = 'bsc'
    MASTER = 'msc'
    LEVEL_CHOICES = (
        (BACH, __('Bsc')),
        (MASTER, __('Msc'))
    )
    name_da = models.CharField(_('Degree name (da)'), max_length=200, blank=True)
    name_en = models.CharField(_('Degree name (en)'), max_length=200, blank=True)
    degree_id_da = models.CharField(_('Degree ID (da)'), max_length=200,
            help_text=_('The degree ID is used to refrence degree in the url @'
                        +' kunet.dk'))
    degree_id_en = models.CharField(_('Degree ID (en)'), max_length=200,
            help_text=_('The degree ID is used to refrence degree in the url @'
                        + ' kunet.dk'), blank=True)
    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_last_edit = models.DateTimeField(_('last edit'), auto_now=True)
    level = models.CharField(max_length=3, choices=LEVEL_CHOICES, default=BACH)

    class Meta:
        verbose_name = _('degree')
        verbose_name_plural = _('degrees')
        # extend permissions created by django-admin
        permissions = (("view_degree", "Can view degree"),)

    def __unicode__(self):
        return self.name_da or self.name_en


# TODO Implement later
#
# Mulighed for mail til studieservice
# gem ikke ku-brugernavn
# class Comment(models.Model):
#     uuid = UUIDField(auto=True)
#     question = models.ForeignKey(Question, verbose_name=_('question'))
#     comment = models.TextField(_('comment'))
#
#     def __unicode__(self):
#         return self.comment


class Rating(models.Model):
    question = models.ForeignKey(Question, verbose_name=_('question'))
    rating = models.BooleanField(_('rating'))
    ku_user = models.CharField(_('KU user'), max_length=6)
    date_added = models.DateTimeField(_('date added'), auto_now_add=True)

    class Meta:
        verbose_name = _('rating')
        verbose_name_plural = _('ratings')

    def __unicode__(self):
        return self.rating

    def clean(self):
        pattern = r'^[b-df-hj-np-tv-z]{3}\d{3}$'
        if len(self.ku_user) != 6 or not re.search(pattern, self.ku_user):
            raise ValidationError(_('Not a valid KU-username'))

def update_degrees(sender, instance, created, **kwargs):
    if created:
        # TODO update every question with all msc or all bsc set to true
        questions = Question.objects.all()
        for q in questions:
            if q.degree_all_bsc and instance.level == 'bsc':
                q.degrees.add(instance)
            if q.degree_all_msc and instance.level == 'msc':
                q.degrees.add(instance)
            q.save()

post_save.connect(update_degrees, sender=Degree, dispatch_uid="update_degrees")
