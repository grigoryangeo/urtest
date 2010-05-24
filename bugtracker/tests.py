# File encoding: utf-8
"""
В данном файле содержаться тесты форм для приложения bugtracker
"""

from django.test import TestCase
from bugtracker.tests_views import *

from enumerations.models import *
from accounts.models import *
from bugtracker.forms import *
from bugtracker.models import *
from bugtracker.views import *


class NewProject(TestCase):
    """ Класс для тестирования формы добавления проекта """
    fixtures = ['users.json', 'ProjectBug.json']

    def setUp(self):
        self.post = {
            'program_languages': ['6', '7', '8'],
            'description': 'description',
            'doc_languages': ['1', '2'],
            'size': '10000',
            'name': 'Project2',
        }

        self.post_exist = {
            'program_languages': ['6', '8', '7'],
            'description': 'description',
            'doc_languages': ['2', '1'],
            'name': 'Project',
            'size': '10000'
        }

    def test_new_project(self):
        """
        Проверка формы добавления проекта
        ( случай хороших данных)
        """

        try:
            #user.json
            customer = PhysCustomer.objects.get(email='PhisCustomer@gmail.com')
        except:
            print  "Object Not found"
            assert(False)

        form = ProjectForm(self.post)
        assert form.is_valid()
        form.save(customer=customer)

        try:
            project = Project.objects.get(name=self.post['name'])
        except Project.DoesNotExist:
            print  "Object Not found"
            assert(False)

        self.assertEquals([str(program_languages.pk) for program_languages in
            project.program_languages.all().order_by('pk')],
            self.post['program_languages'])
        self.assertEquals([str(doc_languages.pk) for doc_languages in
            project.doc_languages.all().order_by('pk')],
            self.post['doc_languages'])
        self.assertEquals(str(project.size), self.post['size'])
        self.assertEquals(project.description, 'description')

    def test_exist_project(self):
        """ добавляемый проект уже существует """
        form = ProjectForm(self.post_exist)
        assert not form.is_valid()


class NewBug(TestCase):
    """ Класс для тестирования формы добавления бага  """
    fixtures = ['users.json', 'ProjectBug.json']

    def setUp(self):
        self.post = {
            'short_description': 'Name',
            'full_description': 'full_description',
            'finding_description': 'finding_description',
            'severity': '1',
            'test_plan_point':  '0.1.1'
            }

    def test_new_bug(self):
        """
        Проверка формы добавления бага
        ( случай хороших данных)
        """

        try:
            tester = Tester.objects.get(email='tester@gmail.com')
            project = Project.objects.get(name='Project')
        except:
            print  "Object Not found"
            assert(False)

        form = BugForm(self.post)
        assert form.is_valid()
        form.save(tester=tester, project=project)

        try:
            bug = Bug.objects.get(short_description=self.post['short_description'])
        except Bug.DoesNotExist:
            print  "Object Not found"
            assert(False)

        self.assertEquals(bug.full_description, self.post['full_description'])
        self.assertEquals(bug.finding_description, self.post['finding_description'])
        self.assertEquals(str(bug.severity), self.post['severity'])
        self.assertEquals(bug.test_plan_point, self.post['test_plan_point'])
