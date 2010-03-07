from django.db import models


class Tester(models.Model):
    """Модель тестера"""
    user = models.OneToOneField(User, parent_link=True)
    # password находятся в User
    surname = models.CharField("Фамилия", max_length=80)
    first_name = models.CharField("Имя", max_length=30)
    second_name = models.CharField("Отчество", max_length=30, blank=True)
    email = models.EmailField("e-mail", max_length=50)

    osystems = models.ManyToManyField('OSystem',
                                        related_name='testers',
                                        verbose_name="ОС")
    program_languages = models.ManyToManyField('ProgramLang',
                                        related_name='testers',
                                        verbose_name="языки программирования")
    testing_types = models.ManyToManyField('TestingType',
                                        related_name='testers',
                                        verbose_name="виды тестирования")
    browsers = models.ManyToManyField('Browser',
                                        related_name='testers',
                                        verbose_name="браузеры")

    description = models.TextField("о себе", blank=True, max_length=300)
    #foto = models.FileField("фотография", upload_to="/home/media", blank=True, max_length=100)

    def _get_full_name(self):
        full_name = self.user.get_full_name()
        if len(full_name) == 0:
            return self.user.username
        else:
            return self.user.get_full_name()

    name = property(_get_full_name)

    class Meta:
        verbose_name = "тестер"
        verbose_name_plural = "тестеры"

    def __unicode__(self):
        return self.name


class Customer(models.Model):
    """Модель Заказчика"""
    TYPE_CHOICES = (
        ('y', 'Юридическое лицо'),
        ('f', 'Физическое лицо'),
    )
    type = models.CharField("Лицо", max_length=1, choices=TYPE_CHOICES,
                            default='y')

    user = models.OneToOneField(User)
    # password находятся в User

    def get_detail(self):
        if self.type == 'f':
            return self.phys_customer
        else:
            return self.ur_customer

    def _get_full_name(self):
        if self.type == 'f':
            return self.phys_customer.full_name
        else:
            return self.ur_customer.name
    name = property(_get_full_name)

    class Meta:
        verbose_name = "заказчик"
        verbose_name_plural = "заказчики"

    def __unicode__(self):
        return self.user.username


class PhysCustomer(models.Model):
    """Модель физического лица"""

    customer = models.OneToOneField('Customer', related_name='phys_customer',
                                verbose_name="заказчик")
    surname = models.CharField("Фамилия заказчика", max_length=80)
    first_name = models.CharField("Имя заказчика", max_length=30)
    second_name = models.CharField("Отчество заказчика", max_length=50, blank=True)
    email = models.EmailField("e-mail", max_length=50)
    passport_serial = models.IntegerField("Серия паспорта", max_length=4)
    passport_number = models.IntegerField("Номер паспорта", max_length=6)
    passport_when = models.DateField("Дата выдачи")
    passport_who = models.CharField("Кем выдан", max_length=100)
    telefon = models.CharField("Контактный телефон", max_length=50)
    other_connect = models.CharField("Другие контактные данные", max_length=100)
    pay_type = models.ManyToManyField('PayingType', related_name='PhysCustomers',
                                verbose_name="Способ оплаты")
    def _get_full_name(self):
        return "%s %s %s" % (self.surname, self.first_name, self.second_name)
    full_name = property(_get_full_name)

    class Meta:
        verbose_name = "физическое лицо"
        verbose_name_plural = "физические лица"

    def __unicode__(self):
        return self.full_name


class UrCustomer(models.Model):
    """Модель юридического лица"""

    customer = models.OneToOneField('Customer', related_name='ur_customer',
                                verbose_name="заказчик")
    email = models.EmailField("e-mail", max_length=50)
    name = models.CharField("Название компании", max_length=50)
    inn = models.IntegerField("ИНН", max_length=10)
    bank_account = models.IntegerField("Номер счета", max_length=50)
    bank = models.CharField("Банк", max_length=50)
    kpp = models.CharField("КПП", max_length=50)
    bik = models.CharField("БИК", max_length=50)
    correspondent_account = models.CharField("Корреспондентский счет", max_length=50)
    ogrn = models.CharField("ОГРН", max_length=50)
    phone = models.CharField("Контактный телефон компании", max_length=50)
    www = models.URLField("Адрес сайта компании", max_length=100)
    address_ur = models.TextField("Юридический адрес компании", max_length=300)
    description = models.TextField("Информация о компании", max_length=300)
    repr_surname = models.CharField("Фамилия заказчика", max_length=80)
    repr_first_name = models.CharField("Имя заказчика", max_length=30)
    repr_second_name = models.CharField("Отчество заказчика", max_length=50, blank=True)
    repr_phone = models.CharField("Контактный телефон", max_length=50)
    pay_type = models.ManyToManyField('PayingType', related_name='UrCustomers',
        verbose_name="Способ оплаты")

    class Meta:
        verbose_name = "юридическое лицо"
        verbose_name_plural = "юридические лица"

    def __unicode__(self):
        return self.name
