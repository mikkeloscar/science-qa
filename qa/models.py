from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_noop as __

class Question(models.Model):
    question_da = models.CharField(_('question da'), max_length=200, blank=True)
    answer_da = models.TextField(_('answer da'), blank=True)
    question_en = models.CharField(_('question en'), max_length=200, blank=True)
    answer_en = models.TextField(_('answer en'), blank=True)
    categories = models.ManyToManyField('Category', related_name="questions",
            verbose_name=_('Categories'))
    degrees = models.ManyToManyField('Degree', related_name="questions",
            verbose_name=_('Degrees'))
    degree_all_bsc = models.BooleanField(_('All Bsc degrees'), default=False)
    degree_all_msc = models.BooleanField(_('All Msc degrees'), default=False)
    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_last_edit = models.DateTimeField(_('last edit'), auto_now=True)

    class Meta:
        verbose_name = _('question')
        verbose_name_plural = _('questions')
        # extend permissions created by django-admin
        permissions = (("view_question", "Can view question"),)
        ordering = ['question_da', 'question_en']

    def question_(self):
        return self.question_da or self.question_en

    def question(self, lang):
        if lang == "en":
            return self.question_en
        else:
            return self.question_da

    def answer(self, lang):
        if lang == "en":
            return self.answer_en
        else:
            return self.answer_da

    def localeDict(self, lang):
        LANGS = ['da', 'en']
        if lang in LANGS:
            if not self.question(lang) or not self.question(lang):
                return None

            c = self.categories.all()
            cats = [ cat.category_id(lang) for cat in c ]

            categories = []
            for cat in c:
                cat = { 'id': cat.category_id(lang),
                        'name': cat.name(lang),
                        'parents': cat.get_parents(lang, cats) }

                # TODO sort by has num parents
                # if len(parents) > 0:
                #     categories.insert(0, cat)
                # else:
                categories.append(cat)

            result = { 'question': self.question(lang),
                       'answer': self.answer(lang),
                       'categories': categories,
                       'id': self.id }
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
    parents = models.ManyToManyField('self', verbose_name=_('Parent categories'),
            symmetrical=False, blank=True, null=True)
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
        ordering = ['name_da', 'name_en']

    def name(self, lang):
        if lang == "en":
            return self.name_en
        else:
            return self.name_da or self.name_en

    def name_(self):
        return self.__unicode__()

    def category_id(self, lang):
        if lang == "en":
            return self.category_id_en
        else:
            return self.category_id_da

    def get_parents(self, lang, categories):
        parents = []
        for parent in self.parents.all():
            if parent and parent.category_id(lang) in categories:
                p = { 'id': parent.category_id(lang),
                      'name': parent.name(lang),
                      'parents': parent.get_parents(lang, categories) }
                parents.append(p)

        return parents

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
        ordering = ['name_da', 'name_en']

    def name_(self):
        return self.__unicode__()

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
    rating = models.IntegerField(_('rating'))
    ku_user = models.CharField(_('KU user'), max_length=6)
    date_added = models.DateTimeField(_('date added'), auto_now_add=True)

    class Meta:
        verbose_name = _('rating')
        verbose_name_plural = _('ratings')
        unique_together = ('question', 'ku_user')

    def __unicode__(self):
        return str(self.rating)

    def clean(self):
        pattern = r'^[b-df-hj-np-tv-z]{3}\d{3}$'
        if len(self.ku_user) != 6 or not re.search(pattern, self.ku_user):
            raise ValidationError(_('Not a valid KU-username'))
        elif self.rating not in [-1, 1]:
            raise ValidationError(_('Not a valid rating'))


def update_degrees(sender, instance, created, **kwargs):
    if created:
        questions = Question.objects.all()
        for q in questions:
            if q.degree_all_bsc and instance.level == 'bsc':
                q.degrees.add(instance)
            if q.degree_all_msc and instance.level == 'msc':
                q.degrees.add(instance)
            q.save()

post_save.connect(update_degrees, sender=Degree, dispatch_uid="update_degrees")
