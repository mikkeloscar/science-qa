from django import forms
from django.utils.translation import ugettext as _

from django.forms.widgets import CheckboxSelectMultiple

from qa.widgets import FilteredSelectMultiple
from qa.models import Question, Category, Degree

class BootstrapForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'



class QuestionForm(BootstrapForm):
    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['answer_da'].widget.attrs['rows'] = 7
        self.fields['answer_en'].widget.attrs['rows'] = 7
        self.fields['degree_all_bsc'].widget.attrs['class'] = None
        self.fields['degree_all_msc'].widget.attrs['class'] = None
        choices = sorted(self.fields['categories'].choices, key=lambda x: x[1])
        self.fields['categories'].widget = FilteredSelectMultiple(
                _('categories'), False, attrs={'rows': '10'}, choices=choices)

    class Media:
        js = ['/jsi18n/']

    class Meta:
        model = Question

    def clean_answer_da(self):
        question = self.cleaned_data['question_da']
        data = self.cleaned_data['answer_da']

        if question and not data:
            raise forms.ValidationError(_("Please add an answer to "
                                          "the question"))

        return data

    def clean_answer_en(self):
        question = self.cleaned_data['question_en']
        data = self.cleaned_data['answer_en']

        if question and not data:
            raise forms.ValidationError(_("Please add an answer to "
                                          "the question"))

        return data


    def clean(self):
        cleaned_data = super(QuestionForm, self).clean()
        question_da = cleaned_data.get("question_da")
        answer_da = cleaned_data.get("answer_da")
        question_en = cleaned_data.get("question_en")
        answer_en = cleaned_data.get("answer_en")

        if not question_da and not question_en:
            raise forms.ValidationError(_("Fill out at least one "
                "question/answer pair"))

        return cleaned_data


class CategoryForm(BootstrapForm):

    class Meta:
        model = Category

    def clean(self):
        cleaned_data = super(CategoryForm, self).clean()
        name_da = cleaned_data.get("name_da")
        name_en = cleaned_data.get("name_en")

        if not name_da and not name_en:
            raise forms.ValidationError(_("Fill out at least one of the name "
                "fields"))

        return cleaned_data

# Inherit from CategoryForm because they are very much alike
class DegreeForm(CategoryForm):

    class Meta:
        model = Degree
