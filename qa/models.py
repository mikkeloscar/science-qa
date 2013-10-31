from django.db import models
from django.utils.translation import ugettext_lazy as _

from uuidfield import UUIDField

class Question(models.Model):
    uuid = UUIDField(auto=True)
    question_da = models.CharField(_('question da'), max_length=200, blank=True)
    answer_da = models.TextField(_('answer da'), blank=True)
    question_en = models.CharField(_('question en'), max_length=200, blank=True)
    answer_en = models.TextField(_('answer en'), blank=True)
    categories = models.ManyToManyField('Category', related_name="cat+",
            verbose_name=_('categories'))
    degrees = models.ManyToManyField('Degree', related_name="degree+",
            verbose_name=_('degrees'))
    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_last_edit = models.DateTimeField(_('last edit'), auto_now=True)

    class Meta:
        verbose_name = _('question')
        verbose_name_plural = _('questions')

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

    def __unicode__(self):
        return self.question_da or self.question_en


class Category(models.Model):
    name_da = models.CharField(_('category name da'), max_length=200,
            blank=True)
    name_en = models.CharField(_('category name en'), max_length=200,
            blank=True)
    category_id = models.CharField(_('category id'), max_length=200)
    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_last_edit = models.DateTimeField(_('last edit'), auto_now=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def name(self, lang):
        if lang == "en":
            return self.name_en
        else:
            return self.name_da or self.name_en

    def __unicode__(self):
        return self.name_da or self.name_en


class Degree(models.Model):
    name_da = models.CharField(_('degree name da'), max_length=200, blank=True)
    name_en = models.CharField(_('degree name en'), max_length=200, blank=True)
    degree_id = models.CharField(_('degree id'), max_length=200)
    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_last_edit = models.DateTimeField(_('last edit'), auto_now=True)

    class Meta:
        verbose_name = _('degree')
        verbose_name_plural = _('degrees')

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
    date_added = models.DateTimeField(_('date added'), auto_now_add=True)

    class Meta:
        verbose_name = _('rating')
        verbose_name_plural = _('ratings')

    def __unicode__(self):
        return self.rating
