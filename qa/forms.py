from django import forms
from django.utils.translation import ugettext as _

from qa.models import Question


class QuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['answer_da'].widget.attrs['rows'] = 3
        self.fields['answer_en'].widget.attrs['rows'] = 3

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
        # else:
        #     if question_da and not answer_da:
        #         raise forms.ValidationError(_("Please add an answer to the "
        #             "question"))
        #     elif question_en and not answer_en:
        #         raise forms.ValidationError(_("Please add an answer to the "
        #             "question"))

        return cleaned_data
