# File encoding: utf-8
from django import forms
import bugtracker.models as models


class BugForm(forms.ModelForm):
    short_description = forms.CharField(label="Краткое описание")
    class Meta:
	model = models.Bug
	exclude = ['tester', 'status', 'status_comment', 'project']


class ProjectForm(forms.ModelForm):
    class Meta:
	model = models.Project
	exclude = ['customer']


class TesterForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    last_name = forms.CharField(label="Фамилия")
    first_name = forms.CharField(label="Имя")
    second_name = forms.CharField(label="Отчество")

    os = forms.ModelMultipleChoiceField(queryset=models.OSystem.objects.all())
    program_languages = forms.ModelMultipleChoiceField(queryset=models.ProgramLang.objects.all())
    testing_types = forms.ModelMultipleChoiceField(queryset=models.TestingType.objects.all())
    browsers = forms.ModelMultipleChoiceField(queryset=models.Browser.objects.all())


class UrCustomerForm(forms.ModelForm):
    class Meta:
	model = models.UrCustomer


class PhysCustomerForm(forms.ModelForm):
    class Meta:
	model = models.PhysCustomer



# XXX:
# Предпросмотр форм
from django.contrib.formtools.preview import FormPreview
from django.http import HttpResponseRedirect

class StupidFormPreview(FormPreview):
    def done(self, request, cleaned_data):
        return HttpResponseRedirect('/')

