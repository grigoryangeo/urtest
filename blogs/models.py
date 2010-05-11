# File encoding: utf-8
from django.db import models
#from markdown import markdown


class Blog(models.Model):
    """Модель блога"""
    TYPE_CHOICES = (
        ('t', 'Тестер'),
        ('c', 'Заказчик'),
        ('p', 'Проект'),
    )
    type = models.CharField("типа автора", max_length=1, choices=TYPE_CHOICES,
                            default='t')
    title = models.CharField("название", max_length=80)

    class Meta:
        verbose_name = u"блог"
        verbose_name_plural = u"блоги"

    def __unicode__(self):
        return self.name


class BlogMsg(models.Model):
    """Модель сообщения блога"""
    blog = models.ForeignKey(Blog, related_name='msgs',
                             verbose_name="блог", editable=False)
    submit_date = models.DateField("дата", auto_now_add=True)
    title = models.CharField("заголовок", max_length=80)
    msg = models.TextField("сообщение", blank=True, max_length=1000)
    
    class Meta:
        verbose_name = u"сообщение"
        verbose_name_plural = u"сообщения"

    #def save(self, force_insert=False, force_update=False):
    #    self.msg = markdown(self.msg)

    def __unicode__(self):
        return self.name
