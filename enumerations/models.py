# File encoding: utf-8
from django.db import models


class StaticItem(models.Model):
    """Абстрактная модель статического объекта: языка, способа оплаты и т.д."""
    name = models.CharField("название", max_length=30)

    class Meta:
        abstract = True
        ordering = ['name']

    def __unicode__(self):
        return self.name


class OS(StaticItem):
    """Модель операционной системы"""
    class Meta(StaticItem.Meta):
        verbose_name = "операционная система"
        verbose_name_plural = "операционные системы"


class Browser(StaticItem):
    """Модель браузера"""
    class Meta(StaticItem.Meta):
        verbose_name = "браузер"
        verbose_name_plural = "браузеры"


class ProgramLanguage(StaticItem):
    """Модель языка программирования"""
    class Meta(StaticItem.Meta):
        verbose_name = "язык программирования"
        verbose_name_plural = "языки программирования"


class TestingType(StaticItem):
    """Модель вида тестирования"""
    class Meta(StaticItem.Meta):
        verbose_name = "вид тестирования"
        verbose_name_plural = "виды тестирования"


class PayType(StaticItem):
    """Модель вида оплаты"""
    class Meta(StaticItem.Meta):
        verbose_name = "вид оплаты"
        verbose_name_plural = "виды оплаты"


class Language(StaticItem):
    """Модель языка"""
    class Meta(StaticItem.Meta):
        verbose_name = "язык"
        verbose_name_plural = "языки"