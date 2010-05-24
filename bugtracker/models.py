# File encoding: utf-8
from django.db import models
from django.contrib.auth.models import User

from enumerations.models import ProgramLanguage, Language
from accounts.models import Tester, Customer
from blogs.models import Blog

class Project(models.Model):
    """Модель проекта"""
    name = models.CharField("название", max_length=50, unique=True)
    size = models.IntegerField("размер в SLOC")
    program_languages = models.ManyToManyField(ProgramLanguage,
                                        related_name='projects',
                                        verbose_name="язык программирования")
    doc_languages = models.ManyToManyField(Language,
                                        related_name='projects',
                                        verbose_name="язык документации")
    description = models.TextField("описание проекта", max_length=300)
    testers = models.ManyToManyField(Tester, blank=True,
                                        related_name='projects',
                                        verbose_name="тестеры")

    customer = models.ForeignKey(Customer,
                                related_name='projects',
                                verbose_name="заказчик",
                                editable=False)
    submit_date = models.DateField("дата размещения", auto_now_add=True)
    blog = models.OneToOneField(Blog)
    f_name = models.CharField("название файла", max_length=50)
    f_comment = models.TextField("описание файла", max_length=600)

    def add_tester(self, tester):
        self.testers.add(tester)
        self.save(force_update=True)

    def save(self, *args, **kwargs):
        if not self.id:
            # Объект создается, не обновляется
            self.blog = Blog.objects.create(title=self.name)
            # Вызов "настоящего" save
        super(Project, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u"проект"
        verbose_name_plural = u"проекты"

    @models.permalink
    def get_absolute_url(self):
        return ('bugtracker.views.project_detail', (), {'project_id': self.pk})

    @models.permalink
    def get_file_url(self):
        return ('upload/%s_%s' % (self.pk, self.f_name))

    def __unicode__(self):
        return self.name


class Bug(models.Model):
    """Модель бага"""
    SEVERITY_CHOICES = (
        (1, 'Низкая'),
        (2, 'Средняя'),
        (3, 'Высокая'),
    )
    STATUS_CHOICES = (
        ('new', 'Баг не рассматривался'),
        ('reviewed', 'Баг на рассмотрении'),
        ('accepted', 'Баг рассмотрен и признан в качестве бага'),
        ('denied', 'Баг рассмотрен и не признан в качестве бага'),
        ('corrected', 'Баг рассмотрен и устранён'),
    )
    tester = models.ForeignKey(Tester, related_name='bugs',
                                verbose_name="Автор",
                                editable=False)
    project = models.ForeignKey(Project, related_name='bugs',verbose_name="проект",
                                editable=False)

    short_description = models.CharField("краткое описание бага", max_length=100)
    test_plan_point = models.CharField("пункт тест-плана", max_length=100)
    severity = models.SmallIntegerField("критичность", max_length=1, choices=SEVERITY_CHOICES,
                                default=2)
    finding_description = models.TextField("как был получен", max_length=600)
    full_description = models.TextField("детальное описание бага", max_length=600)
    submit_date = models.DateTimeField("дата/время добавления", auto_now_add=True)
    status = models.CharField("статус бага", max_length=10, choices=STATUS_CHOICES,
                                default='new')
    status_comment = models.TextField("примечание к статусу", blank=True, max_length=300)
    status_date = models.DateTimeField("дата/время изменения статуса", auto_now=True)
    f_name = models.CharField("имя файла", max_length=50)
    f_comment = models.TextField("описание файла", max_length=600)

    class Meta:
        verbose_name = u"баг"
        verbose_name_plural = u"баги"

    @property
    def name(self):
        return self.short_description

    @models.permalink
    def get_absolute_url(self):
        return ('bugtracker.views.bug_detail', (), {'bug_id': self.pk})

    @models.permalink
    def get_file_url(self):
        return ('upload/%s_%s_%s' % (self.project.pk, self.pk, self.f_name))

    def __unicode__(self):
        return self.name


