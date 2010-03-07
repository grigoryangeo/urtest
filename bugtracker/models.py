# File encoding: utf-8
from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    """Модель проекта"""

    customer = models.ForeignKey('Customer', related_name='projects',
                                verbose_name="заказчик")
    name = models.CharField("название", max_length=50)
    size = models.IntegerField("размер в SLOC", max_length=50)
    program_language = models.ManyToManyField('ProgramLang',
                                        related_name='projects',
                                        verbose_name="язык программирования")
    document_languages = models.ManyToManyField('Language',
                                        related_name='projects',
                                        verbose_name="язык документации")
    project_description = models.TextField("описание проекта", max_length=300)
    testers = models.ManyToManyField('Tester', blank=True,
                                        related_name='projects',
                                        verbose_name="тестеры")
    submit_date = models.DateField("дата размещения", auto_now_add=True)

    #file = models.FileField("исполняемый файл", upload_to="/home/media", blank=True)
    #file_description = models.TextField("описание файла", max_length=300, blank=True)

    def add_tester(self, tester):
        if tester in self.testers.all():
            return
        self.testers.add(tester)
        self.save(force_update=True)

    class Meta:
        verbose_name = "проект"
        verbose_name_plural = "проекты"

    def __unicode__(self):
        return self.name


class Bug(models.Model):
    """Модель бага"""
    SEVERITY_CHOICES = (
        ('l', 'Низкая'),
        ('m', 'Средняя'),
        ('h', 'Высокая'),
    )
    STATUS_CHOICES = (
        ('new', 'Баг не рассматривался'),
        ('reviewed', 'Баг на рассмотрении'),
        ('accepted', 'Баг рассмотрен и признан в качестве бага'),
        ('denied', 'Баг рассмотрен и не признан в качестве бага'),
        ('corrected', 'Баг рассмотрен и устранён'),
    )
    tester = models.ForeignKey('Tester', related_name='bugs',
                                verbose_name="Автор")
    short_description = models.CharField("краткое описание бага", max_length=100)
    test_plan_point = models.CharField("пункт тест-плана", max_length=100)
    severity = models.CharField("критичность", max_length=1, choices=SEVERITY_CHOICES)
    finding_description = models.TextField("как был получен", max_length=600)
    full_description = models.TextField("детальное описание бага", max_length=600)
    #file = models.FileField("файл", upload_to="/home/media", blank=True, max_length=100)
    #commet = models.TextField("комментарии к файлу", blank=True, max_length=150)
    submit_date = models.DateTimeField("дата/время добавления", auto_now_add=True)
    status = models.CharField("статус бага", max_length=10, choices=STATUS_CHOICES,
                                default='new')
    status_comment = models.TextField("примечание к статусу", blank=True, max_length=300)
    status_date = models.DateTimeField("дата/время изменения статуса", auto_now=True)


    project = models.ForeignKey('Project', related_name='bugs',
                                verbose_name="проект")

    def _get_name(self):
        return self.short_description
    name = property(_get_name)

    class Meta:
        verbose_name = "баг"
        verbose_name_plural = "баги"

    def __unicode__(self):
        return self.name



